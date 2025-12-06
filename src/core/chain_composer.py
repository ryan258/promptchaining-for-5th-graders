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

from .chain import MinimalChainable
from .main import build_models, prompt
from .artifact_store import ArtifactStore


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

    # Common
    topic: Optional[str] = None  # For artifact storage

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
    total_cost: float = 0.0
    total_tokens: int = 0

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
        output += f"Total Tokens: {self.total_tokens}\n"
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

    def __init__(self, artifact_store: Optional[ArtifactStore] = None):
        """
        Create a chain composer.

        Args:
            artifact_store: Optional artifact store (creates one if not provided)
        """
        self.artifact_store = artifact_store or ArtifactStore()
        self.client, self.model_names = build_models()
        self.model_info = (self.client, self.model_names[0])

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
        print("🎼 Starting Chain Composition")
        print(f"   Steps: {len(steps)}")
        print()

        global_context = global_context or {}
        steps_executed = []

        for i, step in enumerate(steps, 1):
            print(f"🔗 Step {i}/{len(steps)}: {step.name}")
            print(f"   Type: {step.step_type}")

            step_result = None

            if step.step_type == "tool":
                step_result = self._execute_tool_step(step, global_context)
            elif step.step_type == "chain":
                step_result = self._execute_chain_step(step, global_context)
            elif step.step_type == "synthesize":
                step_result = self._execute_synthesize_step(step, global_context)
            else:
                raise ValueError(f"Unknown step type: {step.step_type}")

            steps_executed.append(step_result)
            print(f"   ✅ Complete")
            print()

        # Gather all artifacts
        all_artifacts = {}
        for key, value in self.artifact_store.artifacts.items():
            all_artifacts[key] = value

        result = CompositionResult(
            steps_executed=steps_executed,
            final_artifacts=all_artifacts,
            execution_trace=self.execution_trace,
            total_tokens=self.total_tokens
        )

        print("🎉 Composition Complete!")
        print()
        print(result.visualize())

        return result

    def _execute_tool_step(
        self,
        step: ChainStep,
        global_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool (like concept_simplifier or subject_connector).
        """
        tool_name = step.tool_name
        tool_args = {**global_context, **step.tool_args}

        print(f"   Running tool: {tool_name}")
        print(f"   Args: {tool_args}")

        # Import the tool dynamically
        tool_path = self._find_tool_path(tool_name)
        if not tool_path:
            raise ValueError(f"Tool not found: {tool_name}")

        # Load the tool module
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the main function (assumes it's named the same as the file)
        tool_func = getattr(module, tool_name)

        # Inject artifact store into the tool
        # This is a bit hacky - we're modifying the tool's execution
        # In practice, tools should accept artifact_store as a parameter

        # For now, we'll execute the tool with its normal signature
        # and rely on it creating artifacts
        if tool_name == "concept_simplifier":
            topic = tool_args.get("topic")
            context = tool_args.get("additional_context", "")
            tool_func(topic, context)

            artifacts_created = [
                f"{self.artifact_store._normalize_key(topic)}:expert_educator",
                f"{self.artifact_store._normalize_key(topic)}:master_communicator"
            ]
        elif tool_name == "subject_connector":
            subject_a = tool_args.get("subject_a")
            subject_b = tool_args.get("subject_b")
            tool_func(subject_a, subject_b)

            topic_key = f"{subject_a}_vs_{subject_b}"
            artifacts_created = [
                f"{self.artifact_store._normalize_key(topic_key)}:polymath_and_innovation_consultant"
            ]
        else:
            artifacts_created = []

        return {
            "name": step.name,
            "type": "tool",
            "tool_name": tool_name,
            "artifacts_created": artifacts_created
        }

    def _execute_chain_step(
        self,
        step: ChainStep,
        global_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a custom chain of prompts.
        """
        context = {**global_context, **step.context}

        print(f"   Running {len(step.prompts)} prompts")

        result, prompts, usage = MinimalChainable.run(
            context=context,
            model=self.model_info,
            callable=prompt,
            prompts=step.prompts,
            return_usage=True,
            artifact_store=self.artifact_store,
            topic=step.topic or step.name
        )

        # Track tokens
        total_step_tokens = 0
        for u in usage:
            if isinstance(u, dict):
                total_step_tokens += u.get('prompt_tokens', 0) + u.get('completion_tokens', 0)

        self.total_tokens += total_step_tokens

        # Get artifacts created
        topic_key = self.artifact_store._normalize_key(step.topic or step.name)
        artifacts_created = [
            key for key in self.artifact_store.artifacts.keys()
            if key.startswith(f"{topic_key}:")
        ]

        return {
            "name": step.name,
            "type": "chain",
            "prompts_count": len(step.prompts),
            "tokens": total_step_tokens,
            "artifacts_created": artifacts_created
        }

    def _execute_synthesize_step(
        self,
        step: ChainStep,
        global_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a synthesis step that combines artifacts.
        """
        pattern = step.artifact_pattern or "*:*"

        print(f"   Synthesizing artifacts matching: {pattern}")

        matching_artifacts = self.artifact_store.query(pattern)

        print(f"   Found {len(matching_artifacts)} artifacts")

        # Build a synthesis prompt that references all matching artifacts
        artifact_refs = "\n".join([
            f"- {key}: {{{{artifact:{key.replace(':', ':')}}}}}"
            for key in matching_artifacts.keys()
        ])

        synthesis_prompt = f"""You are a synthesis expert.

Analyze these artifacts and find emergent patterns:

{artifact_refs}

What insights emerge when you view them together?
What patterns appear across all of them?

Respond in JSON:
{{
  "patterns": ["Pattern 1", "Pattern 2", "Pattern 3"],
  "meta_insights": "Overall insight from combining all artifacts",
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}}"""

        context = {**global_context, **step.context}

        result, prompts, usage = MinimalChainable.run(
            context=context,
            model=self.model_info,
            callable=prompt,
            prompts=[synthesis_prompt],
            return_usage=True,
            artifact_store=self.artifact_store,
            topic=step.topic or "synthesis"
        )

        # Track tokens
        total_step_tokens = 0
        for u in usage:
            if isinstance(u, dict):
                total_step_tokens += u.get('prompt_tokens', 0) + u.get('completion_tokens', 0)

        self.total_tokens += total_step_tokens

        return {
            "name": step.name,
            "type": "synthesize",
            "artifacts_analyzed": list(matching_artifacts.keys()),
            "tokens": total_step_tokens,
            "result": result[0] if result else None
        }

    def _find_tool_path(self, tool_name: str) -> Optional[str]:
        """Find the file path for a tool."""
        # Look in tools/learning/
        learning_path = f"tools/learning/{tool_name}.py"
        if os.path.exists(learning_path):
            return os.path.abspath(learning_path)

        # Look in tools/
        tools_path = f"tools/{tool_name}.py"
        if os.path.exists(tools_path):
            return os.path.abspath(tools_path)

        return None


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
                tool_args={"topic": topic_a}
            ),
            ChainStep(
                name=f"Analyze {topic_b}",
                step_type="tool",
                tool_name="concept_simplifier",
                tool_args={"topic": topic_b}
            ),
            ChainStep(
                name="Find connections",
                step_type="tool",
                tool_name="subject_connector",
                tool_args={"subject_a": topic_a, "subject_b": topic_b}
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
                tool_args={"topic": topic}
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
                }
            ))

        # Step 3: Synthesize into curriculum
        steps.append(ChainStep(
            name="Build learning path",
            step_type="chain",
            topic="curriculum",
            prompts=[
                f"""You are a curriculum designer.

Based on these topics and their connections:
{', '.join(topics)}

And these artifacts showing what we've learned:
{{{{artifact:*:expert_educator}}}}

Design a 4-week learning curriculum.

For each week:
- Learning objectives (what they'll understand)
- Key concepts (from the artifacts)
- Practice exercises
- How it builds on previous weeks

Respond in JSON:
{{
  "weeks": [
    {{
      "week": 1,
      "topic": "...",
      "objectives": ["...", "..."],
      "key_concepts": ["...", "..."],
      "exercises": ["...", "..."]
    }}
  ]
}}"""
            ]
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
            step_type="chain",
            topic=f"{topic}_progression",
            prompts=[
                f"""You are a learning science expert.

Analyze how explanations of '{topic}' progress across levels:

{{{{artifact:*:step_1}}}}

What pedagogical principles are at work?
How does complexity increase appropriately?

Respond in JSON:
{{
  "progression_patterns": ["Pattern 1", "Pattern 2"],
  "scaffolding_techniques": ["Technique 1", "Technique 2"],
  "optimal_learning_path": "Recommendation for learners"
}}"""
            ]
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
