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

def crisis_opportunity_demo():
    print("🚀 Running: Crisis Opportunity Scanner Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Crisis Event
    crisis = "A massive cyberattack shuts down the national power grid for 3 days."
    print(f"Analyzing Crisis: '{crisis}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"crisis": crisis},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Actors
            """Analyze the crisis: '{{crisis}}'.
            Who has been waiting for an event like this to push their pre-existing agenda?
            (e.g., Surveillance hawks, Grid infrastructure lobbyists). Respond in JSON: {"actor_a": "group", "actor_b": "group"}""",

            # Prompt 2: Predict 'Solutions'
            """What 'solutions' will be proposed that go far beyond fixing the immediate problem?
            (e.g., 'Total internet monitoring' vs 'Better firewalls'). Respond in JSON: {"proposed_solution": "description", "hidden_agenda": "description"}""",

            # Prompt 3: Reveal the Dynamic
            """Explain the 'Never let a crisis go to waste' dynamic here. How does the emergency bypass normal democratic debate?
            Respond in JSON: {"mechanism": "Emergency Powers/Fear", "long_term_impact": "description"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "crisis_opportunity_prompts")
    results_file_base = os.path.join(output_dir, "crisis_opportunity_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("crisis_opportunity_scanner", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        crisis_opportunity_demo()
