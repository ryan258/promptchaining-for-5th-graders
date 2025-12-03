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

def viral_hook_demo():
    print("🚀 Running: Viral Hook Laboratory Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Boring Topic to Spice Up
    boring_topic = "The importance of proper dental flossing techniques"
    print(f"Transforming Topic: {boring_topic}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"topic": boring_topic},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify emotional core
            """Analyze the boring topic '{{topic}}'. What is the deep emotional core or hidden curiosity gap here? Why should a human being actually care? Find the fear, greed, vanity, or surprise hidden inside. Respond in JSON: {"emotional_core": "description", "curiosity_gap": "description"}""",

            # Prompt 2: Generate 10 angles
            """Using the emotional core '{{output[-1].emotional_core}}', generate 10 distinct viral hook angles for '{{topic}}'. Use patterns like 'Contrarian', 'Story', 'Data-backed', 'Negative Visualization', 'How-to', etc. Respond in JSON: {"hooks": [{"angle_type": "type", "hook_text": "text"}, ...]}""",

            # Prompt 3: Predict virality scores
            """Review these hooks: {{output[-1].hooks}}. Predict a 'virality score' (0-10) for each based on click-through potential for a general audience. Be harsh. Respond in JSON: {"scored_hooks": [{"hook_text": "text", "score": 8.5, "reason": "reason"}, ...]}""",

            # Prompt 4: Select top 3 and combine
            """Select the top 3 highest scoring hooks from {{output[-1].scored_hooks}}. Now, try to combine the best elements of them into one 'Super Hook'. Respond in JSON: {"top_3": ["hook1", "hook2", "hook3"], "super_hook": "text"}""",

            # Prompt 5: A/B Test Simulation
            """Simulate an A/B test.
            Option A: '{{topic}}' (Original)
            Option B: '{{output[-1].super_hook}}' (Super Hook)
            
            Predict the click-through rate (CTR) difference and explain WHY Option B wins (or loses). Respond in JSON: {"winner": "Option A or B", "ctr_prediction": "Option A: X%, Option B: Y%", "analysis": "reasoning"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "viral_hook_prompts")
    results_file_base = os.path.join(output_dir, "viral_hook_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("viral_hook_laboratory", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env
    
    if setup_demo_env():
        viral_hook_demo()
