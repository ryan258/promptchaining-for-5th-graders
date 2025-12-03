import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

from chain import MinimalChainable
from main import build_models, prompt

def coalition_fracture_demo():
    print("🚀 Running: Coalition Fracture Simulator Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Party Platform
    platform = "The 'Freedom & Justice Party' supports both unregulated free markets AND strict traditional moral values."
    print(f"Analyzing Platform: '{platform}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"platform": platform},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Factions
            """Analyze the party platform: '{{platform}}'.
            Identify the two distinct factions that make up this coalition. What do they want? Respond in JSON: {"faction_a": "name/desire", "faction_b": "name/desire"}""",

            # Prompt 2: Simulate Wedge Issue
            """Propose a 'Wedge Issue' that would force these two factions to fight each other. 
            (e.g., A law that restricts business on religious grounds). Respond in JSON: {"wedge_issue": "description", "why_it_hurts": "reasoning"}""",

            # Prompt 3: Predict Fracture
            """Simulate the internal debate on this wedge issue. Who leaves the coalition? 
            Respond in JSON: {"fracture_point": "description", "surviving_faction": "Faction A/B"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "coalition_fracture_prompts")
    results_file_base = os.path.join(output_dir, "coalition_fracture_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("coalition_fracture_simulator", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        coalition_fracture_demo()
