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

def media_bias_demo():
    print("🚀 Running: Media Bias Triangulator Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # News Event
    event = "A new study shows that the city's minimum wage hike led to a 2% increase in unemployment but a 10% increase in overall earnings for low-income workers."
    print(f"Analyzing Event: '{event}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"event": event},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Generate Biased Headlines
            """Analyze the event: '{{event}}'.
            Generate 3 headlines:
            1. From a Hard Left outlet (focus on earnings).
            2. From a Hard Right outlet (focus on job loss).
            3. From a Corporate Center outlet (focus on conflict).
            Respond in JSON: {"headline_left": "text", "headline_right": "text", "headline_center": "text"}""",

            # Prompt 2: Identify Omissions
            """For each headline, what fact did they intentionally minimize or omit?
            Respond in JSON: {"omission_left": "text", "omission_right": "text", "omission_center": "text"}""",

            # Prompt 3: Synthesize Ground Truth
            """Synthesize a 'Ground Truth' summary that includes all facts without the emotional framing of any side.
            Respond in JSON: {"ground_truth": "text", "bias_rating": "High/Med/Low"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "media_bias_prompts")
    results_file_base = os.path.join(output_dir, "media_bias_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("media_bias_triangulator", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        media_bias_demo()
