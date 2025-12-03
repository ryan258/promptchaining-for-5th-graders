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

def dream_job_demo():
    print("🚀 Running: Dream Job Reverse Engineer Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Sample Job Posting (could be replaced with a real one)
    job_posting = """
    We are looking for a Senior Product Manager to lead our new AI initiatives.
    You must be scrappy, data-driven, and obsessed with user experience.
    We move fast and break things. We don't care about your degree, we care about what you've shipped.
    Responsibilities:
    - Define product roadmap for AI features
    - Work closely with engineering to ship fast
    - Analyze user data to make decisions
    Requirements:
    - 5+ years of PM experience
    - Experience with LLMs is a plus
    - Ability to thrive in chaos
    """

    print(f"Analyzing Job Posting...\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"job_posting": job_posting},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Decode hidden priorities
            """Analyze this job posting:
            '{{job_posting}}'
            
            Decode the hidden priorities and company culture. What are they *really* looking for that they might not be saying explicitly? Respond in JSON: {"hidden_priorities": ["priority1", "priority2"], "culture_vibe": "description"}""",

            # Prompt 2: Identify decision-maker pain points
            """Based on the priorities {{output[-1].hidden_priorities}} and culture {{output[-1].culture_vibe}}, what keeps the hiring manager up at night? What specific pain points are they hiring this role to solve? Respond in JSON: {"manager_pain_points": ["pain1", "pain2", ...]}""",

            # Prompt 3: Craft application strategy
            """Knowing the pain points {{output[-1].manager_pain_points}}, craft a high-level strategy for applying. What is the 'hook' or 'theme' of the application that will resonate most? Respond in JSON: {"application_theme": "theme", "strategy_angle": "description"}""",

            # Prompt 4: Generate resume bullets
            """Using the strategy '{{output[-1].strategy_angle}}', write 3 powerful resume bullet points that prove I can solve their pain points ({{output[-2].manager_pain_points}}). Use strong action verbs and quantify results where possible. Respond in JSON: {"resume_bullets": ["bullet1", "bullet2", "bullet3"]}""",

            # Prompt 5: Draft interview stories
            """Finally, for the resume bullets {{output[-1].resume_bullets}}, draft a brief 'STAR' (Situation, Task, Action, Result) story concept for an interview that backs up the claims. Respond in JSON: {"interview_stories": [{"bullet": "bullet1", "star_story": "story concept"}, ...]}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "dream_job_prompts")
    results_file_base = os.path.join(output_dir, "dream_job_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("dream_job_reverse_engineer", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        dream_job_demo()
