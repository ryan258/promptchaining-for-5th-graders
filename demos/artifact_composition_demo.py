#!/usr/bin/env python3
"""
🔗 Artifact Composition Demo

This demonstrates the power of artifacts:
1. Run concept_simplifier on two topics
2. Use those artifacts in a new chain that compares them
3. Show how chains can build on previous knowledge

This is "chains of chains" - the foundation of meta-learning.
"""

import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chain import MinimalChainable
from main import build_models, prompt
from artifact_store import ArtifactStore


def artifact_composition_demo():
    """
    Demonstrates how artifacts from one chain can feed into another.
    """
    print("=" * 70)
    print("🔗 ARTIFACT COMPOSITION DEMO")
    print("=" * 70)
    print()
    print("This demo shows how chains can build on each other's knowledge.")
    print("We'll create artifacts for two topics, then synthesize them.")
    print()

    # Create a shared artifact store
    artifact_store = ArtifactStore()

    client, model_names = build_models()
    model_info = (client, model_names[0])

    # ========================================================================
    # STEP 1: Analyze first topic and save artifacts
    # ========================================================================
    topic_a = "Neural Networks"

    print(f"📖 Step 1: Analyzing '{topic_a}'...")
    print()

    result_a, prompts_a, usage_a = MinimalChainable.run(
        context={"topic": topic_a},
        model=model_info,
        callable=prompt,
        return_usage=True,
        artifact_store=artifact_store,
        topic=topic_a,
        prompts=[
            """You are an expert educator.

Decompose '{{topic}}' into 3-5 essential components.

For each component, explain in 1-2 clear sentences.

Respond in JSON:
{
  "components": [
    {"name": "Component name", "explanation": "Clear explanation"}
  ]
}""",
            """You are a master communicator.

For each component of '{{topic}}', create ONE powerful analogy.

Components: {{output[-1].components}}

Respond in JSON:
{
  "analogies": [
    {
      "component": "Component name",
      "analogy": "Detailed analogy (2-3 sentences)"
    }
  ]
}"""
        ]
    )

    print(f"✅ Created artifacts for '{topic_a}'")
    print()

    # ========================================================================
    # STEP 2: Analyze second topic and save artifacts
    # ========================================================================
    topic_b = "Human Brain"

    print(f"📖 Step 2: Analyzing '{topic_b}'...")
    print()

    result_b, prompts_b, usage_b = MinimalChainable.run(
        context={"topic": topic_b},
        model=model_info,
        callable=prompt,
        return_usage=True,
        artifact_store=artifact_store,
        topic=topic_b,
        prompts=[
            """You are an expert educator.

Decompose '{{topic}}' into 3-5 essential components.

For each component, explain in 1-2 clear sentences.

Respond in JSON:
{
  "components": [
    {"name": "Component name", "explanation": "Clear explanation"}
  ]
}""",
            """You are a master communicator.

For each component of '{{topic}}', create ONE powerful analogy.

Components: {{output[-1].components}}

Respond in JSON:
{
  "analogies": [
    {
      "component": "Component name",
      "analogy": "Detailed analogy (2-3 sentences)"
    }
  ]
}"""
        ]
    )

    print(f"✅ Created artifacts for '{topic_b}'")
    print()

    # ========================================================================
    # STEP 3: Visualize the artifact store
    # ========================================================================
    print("📚 Artifact Store State:")
    print(artifact_store.visualize())

    # ========================================================================
    # STEP 4: Create a NEW chain that uses artifacts from both topics
    # ========================================================================
    print("🔗 Step 3: Synthesizing insights using artifacts from both topics...")
    print()
    print("This chain references artifacts without re-running the previous chains!")
    print()

    synthesis_result, synthesis_prompts, synthesis_usage = MinimalChainable.run(
        context={
            "topic_a": topic_a,
            "topic_b": topic_b
        },
        model=model_info,
        callable=prompt,
        return_usage=True,
        artifact_store=artifact_store,
        topic=f"{topic_a}_vs_{topic_b}",
        prompts=[
            """You are a comparative analyst.

Compare the components of these two topics:

Topic A ({{topic_a}}):
{{artifact:neural_networks:expert_educator}}

Topic B ({{topic_b}}):
{{artifact:human_brain:expert_educator}}

Find 3 deep structural similarities (not just surface-level comparisons).

Respond in JSON:
{
  "similarities": [
    {
      "aspect": "What's similar",
      "topic_a_component": "Specific component from A",
      "topic_b_component": "Specific component from B",
      "insight": "Why this connection matters"
    }
  ]
}""",
            """You are a synthesis expert.

Based on these similarities:
{{output[-1].similarities}}

And these analogies from each topic:

{{topic_a}} analogies:
{{artifact:neural_networks:master_communicator}}

{{topic_b}} analogies:
{{artifact:human_brain:master_communicator}}

Create a unified explanation that teaches BOTH topics together.

Explain in 4-6 sentences how understanding one helps understand the other.

Respond in JSON:
{
  "unified_explanation": "Your synthesis",
  "key_insight": "The most profound connection between them"
}"""
        ]
    )

    print("=" * 70)
    print("🎯 SYNTHESIS RESULT")
    print("=" * 70)
    print()

    if isinstance(synthesis_result[-1], dict):
        print("📊 Unified Explanation:")
        print(synthesis_result[-1].get("unified_explanation", ""))
        print()
        print("💡 Key Insight:")
        print(synthesis_result[-1].get("key_insight", ""))
    else:
        print(synthesis_result[-1])

    print()
    print("=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)
    print()
    print("What just happened:")
    print("1. Two separate chains analyzed different topics")
    print("2. Each chain saved artifacts (components, analogies)")
    print("3. A third chain used {{artifact:...}} to access that knowledge")
    print("4. NO re-computation needed - artifacts are persistent!")
    print()
    print("This is the foundation for:")
    print("  - Meta-learning (chains that learn from chains)")
    print("  - Knowledge accumulation (every run adds value)")
    print("  - Chain composition (complex workflows from simple parts)")
    print()
    print(f"📁 All artifacts saved to: {artifact_store.base_dir}/")
    print()


if __name__ == "__main__":
    artifact_composition_demo()
