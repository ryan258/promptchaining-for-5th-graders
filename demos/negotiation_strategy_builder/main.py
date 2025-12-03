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

def negotiation_demo():
    print("🚀 Running: Negotiation Strategy Builder Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Negotiation Scenario
    scenario = "I am a freelance graphic designer negotiating a contract with a new startup client. They have a limited budget but promise 'great exposure'. I want a fair market rate."
    print(f"Analyzing Scenario: {scenario}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"scenario": scenario},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Power Analysis
            """Analyze the negotiation scenario: '{{scenario}}'.
            Who has the leverage? What are the hidden power dynamics? Respond in JSON: {"leverage_analysis": "description", "my_power": "high/medium/low", "their_power": "high/medium/low"}""",

            # Prompt 2: BATNA Identification
            """Based on the analysis, define the BATNA (Best Alternative to a Negotiated Agreement) for both sides. What will likely happen if no deal is made? Respond in JSON: {"my_batna": "description", "their_batna": "description"}""",

            # Prompt 3: Anchoring Strategy
            """Given the leverage ({{output[-2].leverage_analysis}}) and BATNAs ({{output[-1].my_batna}} vs {{output[-1].their_batna}}), determine the optimal opening anchor. Should I speak first? What number/terms should I propose? Respond in JSON: {"speak_first": "yes/no", "opening_anchor": "proposal", "reasoning": "why"}""",

            # Prompt 4: Predict Objections
            """I propose the anchor: '{{output[-1].opening_anchor}}'. Predict the top 3 hardest objections the client will raise, especially regarding their 'limited budget'. Respond in JSON: {"objections": ["objection1", "objection2", "objection3"]}""",

            # Prompt 5: Counter-Scripts
            """For the objections {{output[-1].objections}}, script specific, professional responses that pivot back to value without caving on price. Respond in JSON: {"scripts": [{"objection": "objection1", "response_script": "script"}, ...]}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "negotiation_prompts")
    results_file_base = os.path.join(output_dir, "negotiation_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("negotiation_strategy_builder", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        negotiation_demo()
