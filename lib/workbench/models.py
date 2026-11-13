"""The small, versioned contract used by the editor, runner and backups."""

from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, field_validator, model_validator


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return uuid4().hex


def validate_timestamp(value: str) -> str:
    stamp = datetime.fromisoformat(value)
    # Keep enough room for time zone conversion when dates are displayed.
    if stamp.utcoffset() is None or not 1 < stamp.year < 9999:
        raise ValueError("Use a valid date and time with a time zone.")
    return value


Timestamp = Annotated[str, Field(max_length=50), AfterValidator(validate_timestamp)]
RecordId = Annotated[str, Field(pattern=r"^[a-f0-9]{32}$")]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Step(Record):
    name: str = Field(min_length=1, max_length=100)
    purpose: str = Field(default="", max_length=400)
    prompt: str = Field(min_length=1, max_length=8000)

    @field_validator("name", "prompt")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("A step needs both a name and a prompt.")
        return value.strip()


class Recipe(Record):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=600)
    audience: str = Field(default="A curious fifth grader", max_length=200)
    steps: list[Step] = Field(min_length=1, max_length=8)

    @field_validator("title")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Give your recipe a name.")
        return value.strip()


class SavedRecipe(Record):
    id: RecordId = Field(default_factory=new_id)
    created_at: Timestamp = Field(default_factory=now)
    recipe: Recipe
    topic: str = Field(default="", max_length=3000)
    context: str = Field(default="", max_length=16000)
    review_each: bool = True


class ModelSettings(Record):
    max_tokens: int = Field(ge=64, le=12000)
    temperature: float = Field(ge=0, le=2, allow_inf_nan=False)
    timeout_seconds: float = Field(ge=1, le=120, allow_inf_nan=False)


class Result(Record):
    prompt: str = Field(max_length=120000)
    output: str = Field(min_length=1, max_length=60000)
    prompt_tokens: int | None = Field(default=None, ge=0)
    completion_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    seconds: float = Field(default=0, ge=0, allow_inf_nan=False)
    edited: bool = False
    original_output: str | None = Field(default=None, max_length=60000)
    attempt_id: RecordId | None = None
    finish_reason: str | None = Field(default=None, max_length=100)
    response_id: str | None = Field(default=None, max_length=200)
    response_model: str | None = Field(default=None, max_length=200)
    model_settings: ModelSettings | None = None

    @property
    def reported_tokens(self) -> int | None:
        if self.total_tokens is not None:
            return self.total_tokens
        # Older versions serialized missing usage as zero for both counts.
        return sum((self.prompt_tokens or 0, self.completion_tokens or 0)) or None

    @property
    def usage_complete(self) -> bool:
        return self.total_tokens is not None or (
            self.prompt_tokens is not None
            and self.completion_tokens is not None
            and self.reported_tokens is not None
        )


RunState = Literal["ready", "running", "paused", "failed", "interrupted", "completed"]


class Run(Record):
    id: RecordId = Field(default_factory=new_id)
    created_at: Timestamp = Field(default_factory=now)
    updated_at: Timestamp = Field(default_factory=now)
    recipe: Recipe
    topic: str = Field(min_length=1, max_length=3000)
    context: str = Field(default="", max_length=16000)
    model: str = Field(default="", max_length=200)
    mode: Literal["live", "example", "practice", "lab"] = "live"
    practice_case: str | None = Field(default=None, max_length=80, pattern=r"^[a-z0-9][a-z0-9-]*$")
    state: RunState = "ready"
    review_each: bool = True
    pause_requested: bool = False
    results: list[Result] = Field(default_factory=list, max_length=8)
    error: str = Field(default="", max_length=2000)
    review_notice: str = Field(default="", max_length=400)
    revision: int = Field(default=0, ge=0)
    execution_id: RecordId | None = None
    active_attempt_id: RecordId | None = None
    resume_note: str = Field(default="", max_length=1000)
    archived: bool = False
    parent_run_id: RecordId | None = None
    forked_after_step: int | None = Field(default=None, ge=0, le=7)

    @model_validator(mode="after")
    def consistent_steps(self):
        if len(self.results) > len(self.recipe.steps):
            raise ValueError("A run has more results than steps.")
        if self.state == "completed" and len(self.results) != len(self.recipe.steps):
            raise ValueError("A completed run must have every step saved.")
        if self.state != "completed" and len(self.results) == len(self.recipe.steps):
            raise ValueError("A run with every result must be completed.")
        if self.mode == "example" and self.state != "completed":
            raise ValueError("Worked examples must be complete.")
        if (self.mode == "practice") != (self.practice_case is not None):
            raise ValueError("Only practice runs have a practice case.")
        if self.mode == "practice" and self.state == "running":
            raise ValueError("Practice runs cannot dispatch requests.")
        if self.mode == "lab" and (
            not 2 <= len(self.recipe.steps) <= 5
            or self.state not in {"ready", "paused", "completed"}
            or (self.state == "ready" and self.results)
        ):
            raise ValueError("A Chain Lab run needs 2–5 steps and saves only human answers.")
        if self.state != "running" and (self.execution_id or self.active_attempt_id):
            raise ValueError("Only a running chain can have an active execution.")
        if self.active_attempt_id and not self.execution_id:
            raise ValueError("A dispatched step must belong to an active execution.")
        if self.archived and self.state == "running":
            raise ValueError("Pause the run before archiving it.")
        if (self.parent_run_id is None) != (self.forked_after_step is None):
            raise ValueError("A checkpoint fork needs both a source run and a saved step number.")
        if self.forked_after_step is not None:
            valid_fork = (
                self.mode == "live" and 1 <= self.forked_after_step <= len(self.results)
                and self.forked_after_step < len(self.recipe.steps)
            )
            valid_remix = self.mode == "lab" and self.forked_after_step == 0
            if self.parent_run_id == self.id or not (valid_fork or valid_remix):
                raise ValueError("A live branch starts from a saved step. A Chain Lab remix starts from the beginning.")
        return self

    @property
    def total_tokens(self) -> int | None:
        if self.mode != "live":
            return 0
        own_results = self.results[self.forked_after_step or 0:]
        totals = [value for result in own_results if (value := result.reported_tokens) is not None]
        return sum(totals) if totals else None

    @property
    def usage_complete(self) -> bool:
        own_results = self.results[self.forked_after_step or 0:]
        return self.mode != "live" or (bool(own_results) and all(r.usage_complete for r in own_results))


class StepCheckpoint(Record):
    run_id: RecordId
    execution_id: RecordId
    attempt_id: RecordId | None = None
    result: Result | None = None
    error: str = Field(default="", max_length=2000)

    @model_validator(mode="after")
    def validate_outcome(self):
        if (self.result is None) == (not self.error):
            raise ValueError("A checkpoint needs either an answer or a failure message.")
        if self.result and (not self.attempt_id or self.result.attempt_id != self.attempt_id):
            raise ValueError("An answer must match its dispatched attempt.")
        return self


class Backup(Record):
    format: Literal["prompt-chaining-studio"] = "prompt-chaining-studio"
    version: Literal[1] = 1
    exported_at: Timestamp = Field(default_factory=now)
    recipes: list[SavedRecipe] = Field(default_factory=list, max_length=2000)
    runs: list[Run] = Field(default_factory=list, max_length=2000)

    @field_validator("version", mode="before")
    @classmethod
    def integer_version(cls, value):
        if type(value) is not int:
            raise ValueError("Use a supported integer backup version.")
        return value
