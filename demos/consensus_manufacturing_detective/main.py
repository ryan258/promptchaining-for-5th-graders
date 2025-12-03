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

def consensus_detective_demo():
    print("🚀 Running: Consensus Manufacturing Detective Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # The "Truth"
    truth_claim = "Breakfast is the most important meal of the day."
    print(f"Analyzing Claim: {truth_claim}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"claim": truth_claim},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Trace Origin
            """Analyze the common belief: '{{claim}}'.
            Where did this phrase actually originate? Was it a scientific study? A marketing campaign? Respond in JSON: {"origin": "source", "year": "approx year", "creator": "entity"}""",

            # Prompt 2: Map Incentives
            """Who benefited financially from establishing this consensus? 
            (e.g., Bacon producers, Cereal companies). Respond in JSON: {"beneficiaries": ["Industry 1", "Industry 2"], "financial_incentive": "description"}""",

            # Prompt 3: Reveal the Machinery
            """How was this consensus manufactured? 
            - PR campaigns?
            - Lobbying doctors?
            - Cartoons?
            Respond in JSON: {"methods": ["method 1", "method 2"], "effectiveness": "High/Med/Low"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "consensus_detective_prompts")
    results_file_base = os.path.join(output_dir, "consensus_detective_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("consensus_manufacturing_detective", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found.")
    else:
        consensus_detective_demo()
