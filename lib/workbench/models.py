"""The small, versioned contract used by the editor, runner and backups."""

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return uuid4().hex


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
    id: str = Field(default_factory=new_id, pattern=r"^[a-f0-9]{32}$")
    created_at: str = Field(default_factory=now, max_length=50)
    recipe: Recipe
    topic: str = Field(default="", max_length=3000)
    context: str = Field(default="", max_length=16000)
    review_each: bool = True


class Result(Record):
    prompt: str = Field(max_length=120000)
    output: str = Field(min_length=1, max_length=60000)
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    seconds: float = Field(default=0, ge=0)
    edited: bool = False
    original_output: str | None = Field(default=None, max_length=60000)


RunState = Literal["ready", "running", "paused", "failed", "interrupted", "completed"]


class Run(Record):
    id: str = Field(default_factory=new_id, pattern=r"^[a-f0-9]{32}$")
    created_at: str = Field(default_factory=now, max_length=50)
    updated_at: str = Field(default_factory=now, max_length=50)
    recipe: Recipe
    topic: str = Field(min_length=1, max_length=3000)
    context: str = Field(default="", max_length=16000)
    model: str = Field(default="", max_length=200)
    mode: Literal["live", "example"] = "live"
    state: RunState = "ready"
    review_each: bool = True
    pause_requested: bool = False
    results: list[Result] = Field(default_factory=list, max_length=8)
    error: str = Field(default="", max_length=2000)
    revision: int = Field(default=0, ge=0)

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
        return self

    @property
    def total_tokens(self) -> int:
        return sum(r.prompt_tokens + r.completion_tokens for r in self.results)


class Backup(Record):
    format: Literal["prompt-chaining-studio"] = "prompt-chaining-studio"
    version: Literal[1] = 1
    exported_at: str = Field(default_factory=now, max_length=50)
    recipes: list[SavedRecipe] = Field(default_factory=list, max_length=2000)
    runs: list[Run] = Field(default_factory=list, max_length=2000)
