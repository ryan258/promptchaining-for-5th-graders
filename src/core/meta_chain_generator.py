#!/usr/bin/env python3
"""
🧠 Meta-Chain Generator - Chains That Design Chains

This is Layer 6 of the abstraction stack:
1. Prompts
2. Chains
3. Artifacts
4. Tools
5. Compositions
6. Meta-Chains ← YOU ARE HERE

The meta-chain analyzes your goal and automatically designs
the optimal chain to achieve it.

Example:
    generator = MetaChainGenerator()

    # Describe your goal in plain English
    chain = generator.design_chain(
        goal="Teach quantum physics through historical analogies"
    )

    # It designs the chain automatically
    # Then you can execute it
    result = generator.execute_chain(chain)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from .chain import MinimalChainable
from .main import build_models, prompt
from .artifact_store import ArtifactStore


# ============================================================================
# Cognitive Move Library
# ============================================================================

@dataclass
class CognitiveMove:
    """
    A fundamental cognitive operation that can be used in chains.

    Think of these as "thinking primitives" - basic moves that
    can be composed into complex reasoning.
    """
    name: str  # E.g., "decompose", "analogize", "synthesize"
    description: str  # What this move does
    when_to_use: str  # When is this move appropriate
    prompt_template: str  # Template for generating the actual prompt

    # Examples of successful use
    example_contexts: List[str]

    def generate_prompt(self, context: Dict[str, Any]) -> str:
        """
        Generate an actual prompt from this cognitive move.

        Args:
            context: Variables to fill into the template

        Returns:
            Ready-to-use prompt
        """
        prompt_text = self.prompt_template

        # Replace placeholders
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in prompt_text:
                prompt_text = prompt_text.replace(placeholder, str(value))

        return prompt_text


class CognitiveMoveLibrary:
    """
    Library of fundamental cognitive operations.

    These are the building blocks that meta-chains compose.
    """

    @staticmethod
    def get_all_moves() -> List[CognitiveMove]:
        """Get all available cognitive moves."""
        return [
            CognitiveMove(
                name="decompose",
                description="Break a complex concept into essential components",
                when_to_use="When you need to understand the parts of a whole",
                prompt_template="""You are an expert analyst.

Decompose '{{topic}}' into 3-6 essential components.

For each component, explain what it is and why it matters.

Respond in JSON:
{
  "components": [
    {"name": "Component name", "explanation": "What it is and why it matters"}
  ]
}""",
                example_contexts=["Understanding complex systems", "Learning new concepts"]
            ),

            CognitiveMove(
                name="analogize",
                description="Create powerful analogies to make concepts concrete",
                when_to_use="When abstract concepts need to be made tangible",
                prompt_template="""You are a master communicator.

Create 2-3 powerful analogies for '{{topic}}'.

Draw from everyday experience. Make the mapping explicit.

Respond in JSON:
{
  "analogies": [
    {
      "analogy": "The analogy (2-3 sentences)",
      "maps_to": "What aspect of {{topic}} this illuminates"
    }
  ]
}""",
                example_contexts=["Teaching beginners", "Making abstract concrete"]
            ),

            CognitiveMove(
                name="synthesize",
                description="Combine multiple insights into a unified understanding",
                when_to_use="When you have pieces and need the whole picture",
                prompt_template="""You are a synthesis expert.

Given these insights:
{{inputs}}

Create a unified understanding that shows how they fit together.

Respond in JSON:
{
  "synthesis": "Unified explanation (4-6 sentences)",
  "key_insight": "The most important realization"
}""",
                example_contexts=["Combining multiple perspectives", "Building complete picture"]
            ),

            CognitiveMove(
                name="connect",
                description="Find deep connections between seemingly different concepts",
                when_to_use="When exploring relationships between domains",
                prompt_template="""You are a polymath and pattern recognition expert.

Find 3 deep structural connections between:
- {{concept_a}}
- {{concept_b}}

Look for shared mechanisms, not surface similarities.

Respond in JSON:
{
  "connections": [
    {
      "shared_pattern": "What's similar at a deep level",
      "why_it_matters": "What this reveals"
    }
  ]
}""",
                example_contexts=["Cross-domain learning", "Finding unexpected insights"]
            ),

            CognitiveMove(
                name="critique",
                description="Find flaws, gaps, and weaknesses in reasoning",
                when_to_use="When you need to improve or validate understanding",
                prompt_template="""You are a rigorous critic.

Analyze this explanation:
{{explanation}}

Find:
- Logical flaws
- Missing pieces
- Unclear parts
- Assumptions that need justification

Respond in JSON:
{
  "critiques": [
    {
      "issue": "What's wrong",
      "severity": "critical|important|minor",
      "suggestion": "How to fix it"
    }
  ]
}""",
                example_contexts=["Quality improvement", "Validation"]
            ),

            CognitiveMove(
                name="exemplify",
                description="Create concrete, testable examples",
                when_to_use="When abstract understanding needs grounding",
                prompt_template="""You are a learning designer.

For '{{topic}}', create 2-3 concrete examples that:
- Show the concept in action
- Are specific and detailed
- Help verify understanding

Respond in JSON:
{
  "examples": [
    {
      "scenario": "Concrete situation",
      "how_it_demonstrates": "What aspect this shows"
    }
  ]
}""",
                example_contexts=["Making theory practical", "Building intuition"]
            ),

            CognitiveMove(
                name="historicize",
                description="Trace how understanding evolved over time",
                when_to_use="When context and evolution matter",
                prompt_template="""You are a historian of ideas.

How has our understanding of '{{topic}}' evolved?

Trace 3-4 major shifts in understanding.

Respond in JSON:
{
  "evolution": [
    {
      "era": "Time period",
      "understanding": "How it was viewed then",
      "key_insight": "What changed"
    }
  ]
}""",
                example_contexts=["Understanding paradigm shifts", "Seeing how ideas develop"]
            ),

            CognitiveMove(
                name="problematize",
                description="Identify key questions and challenges",
                when_to_use="When you need to understand what's difficult or unresolved",
                prompt_template="""You are a problem finder.

For '{{topic}}', identify:
- Open questions
- Paradoxes or tensions
- Challenges people face understanding it

Respond in JSON:
{
  "problems": [
    {
      "problem": "The challenge or question",
      "why_it_matters": "Why this is important"
    }
  ]
}""",
                example_contexts=["Deep understanding", "Research directions"]
            ),

            CognitiveMove(
                name="apply",
                description="Show how to use the concept in practice",
                when_to_use="When theory needs to become action",
                prompt_template="""You are a practical application expert.

How do you apply '{{topic}}' in real-world scenarios?

Give 2-3 concrete applications with steps.

Respond in JSON:
{
  "applications": [
    {
      "context": "Where you'd use this",
      "steps": ["Step 1", "Step 2", "Step 3"],
      "expected_outcome": "What you achieve"
    }
  ]
}""",
                example_contexts=["Practical mastery", "Skill development"]
            ),

            CognitiveMove(
                name="compare",
                description="Systematically compare and contrast concepts",
                when_to_use="When you need to understand similarities and differences",
                prompt_template="""You are a comparative analyst.

Compare {{concept_a}} and {{concept_b}}.

Create a systematic comparison:
- Similarities
- Differences
- When to use which

Respond in JSON:
{
  "similarities": ["...", "..."],
  "differences": [
    {
      "dimension": "What you're comparing on",
      "concept_a": "How A works",
      "concept_b": "How B works"
    }
  ],
  "guidance": "When to use which"
}""",
                example_contexts=["Choice between options", "Understanding distinctions"]
            )
        ]

    @staticmethod
    def get_move(name: str) -> Optional[CognitiveMove]:
        """Get a specific cognitive move by name."""
        moves = CognitiveMoveLibrary.get_all_moves()
        for move in moves:
            if move.name == name:
                return move
        return None

    @staticmethod
    def describe_all() -> str:
        """Get a description of all moves for the meta-chain."""
        moves = CognitiveMoveLibrary.get_all_moves()
        descriptions = []

        for move in moves:
            descriptions.append(
                f"- **{move.name}**: {move.description}\n"
                f"  When: {move.when_to_use}"
            )

        return "\n\n".join(descriptions)


# ============================================================================
# Chain Design
# ============================================================================

@dataclass
class ChainDesign:
    """
    A designed chain - the output of the meta-chain generator.
    """
    goal: str  # What the user wants to achieve
    reasoning: str  # Why this chain design makes sense
    cognitive_moves: List[str]  # Sequence of move names
    prompts: List[str]  # Actual prompts to execute
    context: Dict[str, Any]  # Context variables
    metadata: Dict[str, Any]  # Additional info

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON."""
        return json.dumps(self.to_dict(), indent=2)

    def visualize(self) -> str:
        """Pretty print the chain design."""
        output = "🧠 Chain Design\n\n"
        output += f"Goal: {self.goal}\n\n"
        output += f"Reasoning: {self.reasoning}\n\n"
        output += f"Cognitive Moves:\n"

        for i, move in enumerate(self.cognitive_moves, 1):
            output += f"  {i}. {move}\n"

        output += f"\nTotal Steps: {len(self.prompts)}\n"

        return output


# ============================================================================
# Meta-Chain Generator
# ============================================================================

class MetaChainGenerator:
    """
    The chain that designs chains.

    This analyzes your goal and automatically creates an optimal
    chain to achieve it.
    """

    def __init__(self, artifact_store: Optional[ArtifactStore] = None):
        """
        Create a meta-chain generator.

        Args:
            artifact_store: Optional artifact store for the meta-chain itself
        """
        self.artifact_store = artifact_store or ArtifactStore()
        self.client, self.model_names = build_models()
        self.model_info = (self.client, self.model_names[0])

        # Load cognitive move library
        self.move_library = CognitiveMoveLibrary()

    def design_chain(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
        constraints: Optional[List[str]] = None
    ) -> ChainDesign:
        """
        Design a custom chain for a goal.

        Args:
            goal: What you want to achieve (plain English)
            context: Additional context variables
            constraints: Constraints like "max 3 steps" or "must use analogies"

        Returns:
            ChainDesign with the designed chain
        """
        print("🧠 Designing chain...")
        print(f"   Goal: {goal}")
        print()

        context = context or {}
        constraints = constraints or []

        # The meta-chain that designs chains
        meta_prompts = [
            # Step 1: Analyze the goal
            f"""You are a meta-cognitive architect.

Analyze this goal: "{goal}"

Context: {json.dumps(context, indent=2) if context else "None"}

What cognitive operations are needed to achieve it?

Available cognitive moves:
{self.move_library.describe_all()}

Consider:
- What needs to be understood first?
- What insights need to be generated?
- How should pieces combine?
- What's the optimal order?

Constraints: {constraints if constraints else "None"}

Respond in JSON:
{{
  "goal_analysis": "What the user is really asking for",
  "required_operations": [
    {{
      "move": "cognitive move name",
      "why": "Why this move is needed",
      "order_priority": 1-10
    }}
  ],
  "optimal_sequence": ["move1", "move2", "move3"],
  "reasoning": "Why this sequence makes sense"
}}""",

            # Step 2: Generate the actual prompts
            """You are a prompt engineering expert.

Based on this chain design:
{{output[-1]}}

Generate the specific prompts for each cognitive move.

For each move in the optimal_sequence:
- Create a detailed, specific prompt
- Use context variables where appropriate: {context_vars}
- Ensure each prompt builds on previous outputs
- Use {{{{output[-1]}}}} to reference previous steps

Respond in JSON:
{{
  "prompts": [
    {{
      "step": 1,
      "cognitive_move": "move name",
      "prompt": "The full prompt text",
      "uses_previous_output": true/false
    }}
  ]
}}""".replace("{context_vars}", str(list(context.keys())))
        ]

        # Execute the meta-chain
        result, _, _ = MinimalChainable.run(
            context={"goal": goal},
            model=self.model_info,
            callable=prompt,
            prompts=meta_prompts,
            return_usage=True,
            artifact_store=self.artifact_store,
            topic=f"meta_chain_design_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Extract the design
        goal_analysis = result[0]
        prompt_design = result[1]

        # Debug output
        print(f"   Goal analysis type: {type(goal_analysis)}")
        print(f"   Prompt design type: {type(prompt_design)}")

        # Build ChainDesign - handle both dict and string cases
        if isinstance(goal_analysis, dict) and isinstance(prompt_design, dict):
            cognitive_moves = goal_analysis.get("optimal_sequence", [])
            prompts_data = prompt_design.get("prompts", [])
            prompts = [p.get("prompt", "") if isinstance(p, dict) else str(p) for p in prompts_data]
            reasoning = goal_analysis.get("reasoning", "")

            design = ChainDesign(
                goal=goal,
                reasoning=reasoning,
                cognitive_moves=cognitive_moves,
                prompts=prompts,
                context=context,
                metadata={
                    "goal_analysis": goal_analysis,
                    "prompt_design": prompt_design,
                    "generated_at": datetime.now().isoformat()
                }
            )

            print("✅ Chain designed!")
            print()
            print(design.visualize())

            return design
        else:
            # Fallback: create a simple design if meta-chain didn't format correctly
            print("⚠️  Meta-chain returned unexpected format, using fallback")
            print(f"   Goal analysis: {str(goal_analysis)[:100]}")
            print(f"   Prompt design: {str(prompt_design)[:100]}")

            # Create a simple 2-step chain as fallback
            design = ChainDesign(
                goal=goal,
                reasoning="Fallback design due to meta-chain format issue",
                cognitive_moves=["decompose", "synthesize"],
                prompts=[
                    f"Analyze and explain {context.get('topic', goal)} in detail.",
                    "Based on the analysis above, create a concise summary."
                ],
                context=context,
                metadata={
                    "fallback": True,
                    "generated_at": datetime.now().isoformat()
                }
            )

            return design

    def execute_chain(
        self,
        design: ChainDesign,
        artifact_store: Optional[ArtifactStore] = None
    ) -> tuple:
        """
        Execute a designed chain.

        Args:
            design: The ChainDesign to execute
            artifact_store: Optional artifact store for outputs

        Returns:
            Tuple of (outputs, prompts, usage)
        """
        print("🚀 Executing designed chain...")
        print()

        artifact_store = artifact_store or self.artifact_store

        # Execute the chain
        result, prompts, usage = MinimalChainable.run(
            context=design.context,
            model=self.model_info,
            callable=prompt,
            prompts=design.prompts,
            return_usage=True,
            artifact_store=artifact_store,
            topic=design.goal.lower().replace(" ", "_")[:50]
        )

        print("✅ Chain executed!")
        print()

        return result, prompts, usage

    def design_and_execute(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
        constraints: Optional[List[str]] = None
    ) -> tuple:
        """
        Design and execute a chain in one call.

        Args:
            goal: What you want to achieve
            context: Additional context
            constraints: Design constraints

        Returns:
            Tuple of (chain_design, outputs, prompts, usage)
        """
        # Design
        design = self.design_chain(goal, context, constraints)

        # Execute
        outputs, prompts, usage = self.execute_chain(design)

        return design, outputs, prompts, usage


# ============================================================================
# Quick Helpers
# ============================================================================

def quick_generate(goal: str, **context) -> tuple:
    """
    Quick helper to design and execute a chain.

    Usage:
        design, outputs = quick_generate(
            "Explain recursion through analogies",
            topic="recursion"
        )
    """
    generator = MetaChainGenerator()
    design, outputs, prompts, usage = generator.design_and_execute(goal, context)
    return design, outputs


if __name__ == "__main__":
    print("🧠 Meta-Chain Generator")
    print()
    print("This system designs chains automatically.")
    print()
    print("Try:")
    print('  quick_generate("Teach quantum physics through historical analogies")')
    print('  quick_generate("Compare machine learning to human learning")')
    print('  quick_generate("Break down blockchain into teachable parts")')
    print()
