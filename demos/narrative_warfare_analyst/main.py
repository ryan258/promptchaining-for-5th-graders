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

def narrative_warfare_demo():
    print("🚀 Running: Narrative Warfare Analyst Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Competing Narratives
    event = "A new AI model is released that can write perfect code."
    narrative_a = "This is the end of human programming. Millions will be unemployed."
    narrative_b = "This is the democratization of creation. Anyone can now build their dream app."

    print(f"Analyzing Narratives:\nA: {narrative_a}\nB: {narrative_b}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"event": event, "narrative_a": narrative_a, "narrative_b": narrative_b},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Frames
            """Analyze the two narratives about '{{event}}'.
            Narrative A: '{{narrative_a}}'
            Narrative B: '{{narrative_b}}'
            
            What is the underlying 'frame' or emotional trigger for each? Respond in JSON: {"frame_a": "Fear/Hope/etc", "frame_b": "Fear/Hope/etc", "analysis": "description"}""",

            # Prompt 2: Map Beneficiaries
            """Who benefits if Narrative A wins? Who benefits if Narrative B wins? 
            (Think: Unions, Tech Companies, Politicians, etc.) Respond in JSON: {"beneficiaries_a": ["Group 1"], "beneficiaries_b": ["Group 2"]}""",

            # Prompt 3: Predict Winner
            """Which narrative is more likely to go viral and 'win' the public consciousness? Why? 
            (Consider negativity bias vs aspirational thinking). Respond in JSON: {"predicted_winner": "Narrative A/B", "reasoning": "why"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "narrative_warfare_prompts")
    results_file_base = os.path.join(output_dir, "narrative_warfare_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("narrative_warfare_analyst", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found.")
    else:
        narrative_warfare_demo()
