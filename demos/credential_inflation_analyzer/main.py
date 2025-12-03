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

def credential_inflation_demo():
    print("🚀 Running: Credential Inflation Analyzer Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Job Requirement
    job_role = "Entry-Level Data Analyst"
    current_reqs = "Master's degree in Data Science, 3+ years experience with Python/SQL, portfolio of ML projects."
    
    print(f"Analyzing Role: {job_role}\nRequirements: {current_reqs}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"role": job_role, "reqs": current_reqs},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Analyze Current State
            """Analyze the current requirements for '{{role}}': '{{reqs}}'.
            Are these realistic for 'entry-level'? What is the implied barrier to entry? Respond in JSON: {"analysis": "description", "barrier_level": "High/Med/Low"}""",

            # Prompt 2: Historical Trace
            """Estimate the requirements for this same role (or its equivalent like 'Junior Statistician') in the year 2010 and 2000. Respond in JSON: {"reqs_2010": "description", "reqs_2000": "description"}""",

            # Prompt 3: Calculate Inflation
            """Compare {{output[-1].reqs_2000}} vs {{reqs}}. 
            What is the 'inflation rate' of credentials? Why has this happened? (Supply of graduates? Filtering mechanism? Complexity of tools?). Respond in JSON: {"inflation_factor": "X times harder", "primary_cause": "reason"}""",

            # Prompt 4: Predict Future
            """Extrapolate this trend to 2030. What will be required for an 'Entry-Level Data Analyst' then? 
            Will it require a PhD? Or will AI change the game entirely? Respond in JSON: {"prediction_2030": "requirements", "rationale": "reason"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "credential_inflation_prompts")
    results_file_base = os.path.join(output_dir, "credential_inflation_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("credential_inflation_analyzer", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        credential_inflation_demo()
