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

def proxy_war_demo():
    print("🚀 Running: Proxy War Analyst Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Conflict Scenario
    conflict = "In the small nation of 'Mineralia', rebels armed with 'Eagle-1' missiles are fighting a government backed by 'Bear-X' tanks. Mineralia has the world's largest lithium deposits."
    print(f"Analyzing Conflict: '{conflict}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"conflict": conflict},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify External Actors
            """Analyze the conflict: '{{conflict}}'.
            Who manufactures 'Eagle-1' missiles? Who manufactures 'Bear-X' tanks? 
            (Infer the real-world superpowers represented here). Respond in JSON: {"power_a": "Name", "power_b": "Name"}""",

            # Prompt 2: Map Strategic Interests
            """Why do these powers care about 'Mineralia'? It's not about the local politics.
            What is the strategic resource or advantage? Respond in JSON: {"resource": "Lithium/Oil/Location", "strategic_value": "High/Med/Low"}""",

            # Prompt 3: Predict Escalation
            """Predict the next move. Will Power A send peacekeepers or more missiles? 
            Respond in JSON: {"prediction": "description", "reasoning": "why"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "proxy_war_prompts")
    results_file_base = os.path.join(output_dir, "proxy_war_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("proxy_war_analyst", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        proxy_war_demo()
