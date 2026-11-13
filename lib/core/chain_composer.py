#!/usr/bin/env python3
"""
🎼 Chain Composer - Orchestrate Multiple Chains

Build complex workflows by composing simple chains together.
This is "chains of chains" - meta-level prompt engineering.

Example:
    # Build a learning curriculum
    composer = ChainComposer()
    result = composer.compose([
        Step("concept_simplifier", topic="Machine Learning"),
        Step("concept_simplifier", topic="Neural Networks"),
        Step("subject_connector", subject_a="Machine Learning", subject_b="Neural Networks"),
        Step("synthesize", use_artifacts=["*:*"])
    ])
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
import importlib.util
import inspect
from copy import deepcopy
from fnmatch import fnmatchcase
from functools import lru_cache
from pathlib import Path
from uuid import uuid4

from .chain import MinimalChainable
from .errors import InputError
from .limits import MAX_CHAIN_STEPS, validate_prompts
from .llm_client import build_models, request_completion
from .artifact_store import ArtifactStore


@lru_cache(maxsize=1)
def _discover_tool_registry() -> Dict[str, str]:
    """Discover tool modules under the project tool roots. Clear this cache after adding tools at runtime."""
    project_root = Path(__file__).resolve().parents[2]
    roots = [project_root / "tools" / "learning"]
    discovered: Dict[str, str] = {}

    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if path.stem != "__init__":
                discovered[path.stem] = str(path.resolve())

    return discovered


@dataclass
class ChainStep:
    """
    A single step in a composed chain.

    Can be:
    - A tool (concept_simplifier, subject_connector)
    - A custom chain (list of prompts)
    - A reference to artifacts
    """
    name: str  # Step identifier
    step_type: str  # "tool", "chain", "synthesize"

    # For tool type
    tool_name: Optional[str] = None
    tool_args: Dict[str, Any] = field(default_factory=dict)

    # For chain type
    prompts: Optional[List[str]] = None
    context: Dict[str, Any] = field(default_factory=dict)

    # For synthesize type
    artifact_pattern: Optional[str] = None
    synthesis_prompt: Optional[str] = None

    # Common
    topic: Optional[str] = None  # For artifact storage
    scope_output: bool = False

    def __repr__(self):
        if self.step_type == "tool":
            return f"ChainStep(tool={self.tool_name}, args={self.tool_args})"
        elif self.step_type == "chain":
            return f"ChainStep(chain with {len(self.prompts or [])} prompts)"
        else:
            return f"ChainStep({self.step_type})"


@dataclass
class CompositionResult:
    """
    Result of a chain composition.
    """
    steps_executed: List[Dict[str, Any]]  # What happened at each step
    final_artifacts: Dict[str, Any]  # All artifacts created
    execution_trace: List[Dict[str, Any]]  # Detailed trace
    total_cost: Optional[float] = None
    total_tokens: int = 0
    usage_complete: bool = True

    def visualize(self) -> str:
        """Create a text visualization of the composition."""
        output = "🎼 Composition Result\n\n"

        for i, step in enumerate(self.steps_executed, 1):
            output += f"{i}. {step['name']}\n"
            output += f"   Type: {step['type']}\n"
            if 'artifacts_created' in step:
                output += f"   Created: {', '.join(step['artifacts_created'])}\n"
            if 'artifacts_used' in step:
                output += f"   Used: {', '.join(step['artifacts_used'])}\n"
            output += "\n"

        output += f"Total Steps: {len(self.steps_executed)}\n"
        label = "Total reported tokens" if self.usage_complete else "Known token subtotal (some usage unavailable)"
        output += f"{label}: {self.total_tokens}\n"
        output += f"Artifacts Created: {len(self.final_artifacts)}\n"

        return output


class ChainComposer:
    """
    Orchestrates multiple chains together into complex workflows.

    The composer can:
    - Run tools in sequence
    - Execute custom chains
    - Synthesize artifacts
    - Track dependencies
    - Propagate context
    """

    def __init__(
        self,
        artifact_store: Optional[ArtifactStore] = None,
        model_info: Optional[Any] = None,
        llm_callable: Callable = request_completion,
    ):
        """
        Create a chain composer.

        Args:
            artifact_store: Optional artifact store (creates one if not provided)
            model_info: Optional preconfigured (client, model_name) tuple for testability
            llm_callable: Optional callable used by MinimalChainable.run
        """
        self.artifact_store = artifact_store or ArtifactStore()
        self.llm_callable = llm_callable

        if model_info is None:
            self.client, self.model_names = build_models()
            self.model_info = (self.client, self.model_names[0])
        else:
            self.client = None
            self.model_names = []
            self.model_info = model_info

        # Track execution
        self.execution_trace = []
        self.total_tokens = 0

    def compose(
        self,
        steps: List[ChainStep],
        global_context: Optional[Dict[str, Any]] = None
    ) -> CompositionResult:
        """
        Execute a composition of chain steps.

        Args:
            steps: List of ChainStep objects to execute in order
            global_context: Context available to all steps

        Returns:
            CompositionResult with execution details
        """
        if not 1 <= len(steps) <= MAX_CHAIN_STEPS:
            raise InputError(f"Choose 1–{MAX_CHAIN_STEPS} composition steps.")
        for step in steps:
            if step.step_type == "chain":
                validate_prompts(step.prompts)
            elif step.step_type == "tool":
                if not self._find_tool_path(step.tool_name):
                    raise InputError("Choose an installed tool for each tool step.")
            elif step.step_type != "synthesize":
                raise InputError("Choose a tool, chain or synthesis step.")

        print("🎼 Starting Chain Composition")
        print(f"   Steps: {len(steps)}")
        print()

        global_context = global_context or {}
        steps_executed = []
        artifacts_created = {}
        composition_id = uuid4().hex[:12]

        for i, step in enumerate(steps, 1):
            print(f"🔗 Step {i}/{len(steps)}: {step.name}")
            print(f"   Type: {step.step_type}")

            topic = step.topic or step.name
            if step.scope_output or step.step_type == "synthesize":
                topic = f"{topic[:100]}_{composition_id}_step_{i}"

            if step.step_type == "tool":
                step_result = self._execute_tool_step(step, global_context, topic if step.scope_output else None)
            elif step.step_type == "chain":
                step_result = self._execute_chain_step(step, global_context, topic)
            else:
                step_result = self._execute_synthesize_step(step, global_context, topic, artifacts_created)

            steps_executed.append(step_result)
            for key in step_result["artifacts_created"]:
                artifacts_created[key] = self.artifact_store.get_by_key(key)
            print(f"   ✅ Complete")
            print()

        result = CompositionResult(
            steps_executed=steps_executed,
            final_artifacts=artifacts_created,
            execution_trace=deepcopy(steps_executed),
            total_tokens=sum(step.get("tokens", 0) for step in steps_executed),
            usage_complete=all(step.get("usage_complete", True) for step in steps_executed)
        )
        self.execution_trace = deepcopy(steps_executed)
        self.total_tokens = result.total_tokens

        print("🎉 Composition Complete!")
        print()
        print(result.visualize())

        return result

    def _execute_tool_step(
        self,
        step: ChainStep,
        global_context: Dict[str, Any],
        artifact_topic: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a tool (like concept_simplifier or subject_connector).
        """
        tool_name = step.tool_name
        tool_args = {**global_context, **step.tool_args}

        print(f"   Running tool: {tool_name}")


        # Import the tool dynamically
        tool_path = self._find_tool_path(tool_name)
        if not tool_path:
            raise ValueError(f"Tool not found: {tool_name}")

        # Load the tool module
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Unable to load tool module: {tool_name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the main function (assumes it's named the same as the file)
        tool_func = getattr(module, tool_name)

        # Execute tool and track new artifacts
        before_metadata = self.artifact_store.metadata.copy()

        signature = inspect.signature(tool_func)
        call_kwargs = {
            name: value
            for name, value in tool_args.items()
            if name in signature.parameters and name not in {"artifact_store", "artifact_topic", "llm_callable", "model_info", "result_file"}
        }
        dependencies = {"artifact_store": self.artifact_store, "artifact_topic": artifact_topic,
                        "llm_callable": self.llm_callable, "model_info": self.model_info}
        call_kwargs.update({name: value for name, value in dependencies.items() if name in signature.parameters})

        try:
            signature.bind(**call_kwargs)
        except TypeError as exc:
            raise ValueError(f"Invalid arguments for tool '{tool_name}': {exc}") from exc

        tool_result = tool_func(**call_kwargs)
        if (isinstance(tool_result, tuple) and len(tool_result) == 2 and isinstance(tool_result[1], dict)
                and "steps" in tool_result[1]):
            _, trace = tool_result
            return {"name": step.name, "type": "tool", "tool_name": tool_name,
                    **self._trace_summary(trace)}

        artifacts_created = sorted(key for key, meta in self.artifact_store.metadata.copy().items()
                                   if before_metadata.get(key) is not meta)

        return {
            "name": step.name,
            "type": "tool",
            "tool_name": tool_name,
            "artifacts_created": artifacts_created,
            "usage_complete": False,
            "usage_note": "This tool does not return usage to the composer; token total is a known subtotal."
        }

    def _execute_chain_step(
        self,
        step: ChainStep,
        global_context: Dict[str, Any],
        topic: str,
    ) -> Dict[str, Any]:
        """
        Execute a custom chain of prompts.
        """
        context = {**global_context, **step.context}

        print(f"   Running {len(step.prompts)} prompts")

        result, prompts, usage, trace = MinimalChainable.run(
            context=context,
            model=self.model_info,
            llm_callable=self.llm_callable,
            prompts=step.prompts,
            return_trace=True,
            artifact_store=self.artifact_store,
            topic=topic,
        )

        return {
            "name": step.name,
            "type": "chain",
            "prompts_count": len(step.prompts),
            **self._trace_summary(trace),
        }

    def _execute_synthesize_step(
        self,
        step: ChainStep,
        global_context: Dict[str, Any],
        topic: str,
        artifacts_created: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Combine outputs created by earlier steps in this composition.
        """
        pattern = step.artifact_pattern or "*:*"

        print(f"   Synthesizing artifacts matching: {pattern}")

        matching_artifacts = {key: value for key, value in artifacts_created.items() if fnmatchcase(key, pattern)}
        if not matching_artifacts:
            raise InputError("No earlier outputs in this composition match the synthesis inputs.")

        print(f"   Found {len(matching_artifacts)} artifacts")

        synthesis_prompt = step.synthesis_prompt or """You are a synthesis expert.

Analyze these artifacts and find emergent patterns:

{{composition_artifacts}}

What insights emerge when you view them together?
What patterns appear across all of them?

Respond in JSON:
{
  "patterns": ["Pattern 1", "Pattern 2", "Pattern 3"],
  "meta_insights": "Overall insight from combining all artifacts",
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}"""

        context = {**global_context, **step.context, "composition_artifacts": matching_artifacts}

        result, prompts, usage, trace = MinimalChainable.run(
            context=context,
            model=self.model_info,
            llm_callable=self.llm_callable,
            prompts=[synthesis_prompt],
            return_trace=True,
            artifact_store=self.artifact_store,
            topic=topic,
        )

        return {
            "name": step.name,
            "type": "synthesize",
            "artifacts_analyzed": list(matching_artifacts.keys()),
            **self._trace_summary(trace),
            "result": result[0] if result else None
        }

    @staticmethod
    def _trace_summary(trace):
        if trace.get("completion_complete") is False:
            raise InputError("A composition answer did not finish. Review saved artifacts before trying again.")
        return {"trace": trace, "tokens": trace.get("total_tokens", 0),
                "usage_complete": trace.get("usage_complete", False),
                "artifacts_created": [step["artifact_key"] for step in trace.get("steps", []) if "artifact_key" in step]}

    @classmethod
    def refresh_tool_registry(cls) -> None:
        """Clear the cached tool registry after adding or renaming tool files in a live process."""
        _discover_tool_registry.cache_clear()

    def _find_tool_path(self, tool_name: str) -> Optional[str]:
        """Find the file path for an approved tool."""
        return _discover_tool_registry().get(tool_name)


# ============================================================================
# Recipe System - Pre-built compositions
# ============================================================================

class ChainRecipe:
    """
    A pre-built chain composition recipe.

    Recipes are templates for common composition patterns.
    """

    @staticmethod
    def concept_comparison(topic_a: str, topic_b: str) -> List[ChainStep]:
        """
        Recipe: Compare two concepts deeply.

        1. Simplify concept A
        2. Simplify concept B
        3. Find connections
        4. Synthesize insights
        """
        return [
            ChainStep(
                name=f"Analyze {topic_a}",
                step_type="tool",
                tool_name="concept_simplifier",
                tool_args={"topic": topic_a},
                scope_output=True,
            ),
            ChainStep(
                name=f"Analyze {topic_b}",
                step_type="tool",
                tool_name="concept_simplifier",
                tool_args={"topic": topic_b},
                scope_output=True,
            ),
            ChainStep(
                name="Find connections",
                step_type="tool",
                tool_name="subject_connector",
                tool_args={"subject_a": topic_a, "subject_b": topic_b},
                scope_output=True,
            ),
            ChainStep(
                name="Synthesize all insights",
                step_type="synthesize",
                artifact_pattern="*:*",
                topic=f"{topic_a}_and_{topic_b}_synthesis"
            )
        ]

    @staticmethod
    def learning_curriculum(topics: List[str]) -> List[ChainStep]:
        """
        Recipe: Build a learning curriculum from multiple topics.

        1. Simplify each topic
        2. Find connections between adjacent topics
        3. Create a unified learning path
        """
        steps = []

        # Step 1: Analyze each topic
        for topic in topics:
            steps.append(ChainStep(
                name=f"Analyze {topic}",
                step_type="tool",
                tool_name="concept_simplifier",
                tool_args={"topic": topic},
                scope_output=True,
            ))

        # Step 2: Connect adjacent topics
        for i in range(len(topics) - 1):
            steps.append(ChainStep(
                name=f"Connect {topics[i]} → {topics[i+1]}",
                step_type="tool",
                tool_name="subject_connector",
                tool_args={
                    "subject_a": topics[i],
                    "subject_b": topics[i+1]
                },
                scope_output=True,
            ))

        # Step 3: Synthesize into curriculum
        steps.append(ChainStep(
            name="Build learning path",
            step_type="synthesize",
            topic="curriculum",
            context={"topics": topics},
            synthesis_prompt="""You are a curriculum designer.

Based on these topics and their connections:
{{topics}}

Use these artifacts from the preceding steps:
{{composition_artifacts}}

Design a 4-week learning curriculum.

For each week:
- Learning objectives (what they'll understand)
- Key concepts (from the artifacts)
- Practice exercises
- How it builds on previous weeks

Respond in JSON:
{
  "weeks": [
    {
      "week": 1,
      "topic": "...",
      "objectives": ["...", "..."],
      "key_concepts": ["...", "..."],
      "exercises": ["...", "..."]
    }
  ]
}""",
        ))

        return steps

    @staticmethod
    def progressive_depth(topic: str, levels: List[str] = None) -> List[ChainStep]:
        """
        Recipe: Explain a topic at progressive depth levels.

        1. 5th grader explanation
        2. High school explanation
        3. College explanation
        4. Expert explanation
        5. Synthesize the progression
        """
        levels = levels or ["5th grader", "high school student", "college student", "expert"]

        steps = []

        for level in levels:
            steps.append(ChainStep(
                name=f"Explain for {level}",
                step_type="chain",
                topic=f"{topic}_{level.replace(' ', '_')}",
                scope_output=True,
                context={"topic": topic, "level": level},
                prompts=[
                    f"""You are an expert educator.

Explain '{{{{topic}}}}' for a {{{{level}}}}.

Use language and concepts appropriate for this audience.
Include examples they can relate to.

Respond in JSON:
{{
  "explanation": "Your explanation (3-5 sentences)",
  "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
  "example": "A concrete example for this level"
}}"""
                ]
            ))

        # Synthesize the progression
        steps.append(ChainStep(
            name="Analyze learning progression",
            step_type="synthesize",
            topic=f"{topic}_progression",
            context={"topic": topic},
            synthesis_prompt="""You are a learning science expert.

Analyze how explanations of '{{topic}}' progress across levels:

{{composition_artifacts}}

What pedagogical principles are at work?
How does complexity increase appropriately?

Respond in JSON:
{
  "progression_patterns": ["Pattern 1", "Pattern 2"],
  "scaffolding_techniques": ["Technique 1", "Technique 2"],
  "optimal_learning_path": "Recommendation for learners"
}""",
        ))

        return steps


def quick_compose(recipe_name: str, **kwargs) -> CompositionResult:
    """
    Quick helper to run a recipe.

    Usage:
        quick_compose("concept_comparison", topic_a="AI", topic_b="Brain")
    """
    composer = ChainComposer()

    recipe_func = getattr(ChainRecipe, recipe_name, None)
    if not recipe_func:
        raise ValueError(f"Unknown recipe: {recipe_name}")

    steps = recipe_func(**kwargs)
    return composer.compose(steps)


if __name__ == "__main__":
    # Demo
    print("🎼 Chain Composer Demo")
    print()
    print("Try these recipes:")
    print("  - ChainRecipe.concept_comparison('AI', 'Human Brain')")
    print("  - ChainRecipe.learning_curriculum(['Python', 'Data Structures', 'Algorithms'])")
    print("  - ChainRecipe.progressive_depth('Quantum Mechanics')")
    print()
