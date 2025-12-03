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

def architecture_demo():
    print("🚀 Running: Code Architecture Critic Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Sample Code Snippet (Messy Python)
    code_sample = """
    def process_data(data):
        results = []
        for item in data:
            if item['type'] == 'A':
                if item['value'] > 10:
                    results.append(item['value'] * 2)
            elif item['type'] == 'B':
                db_conn = connect_to_db() # Implicit dependency
                db_conn.save(item)
                results.append(True)
        return results
    """
    print(f"Analyzing Code Sample...\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"code": code_sample},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Patterns & Anti-Patterns
            """Analyze this code snippet:
            ```python
            {{code}}
            ```
            Identify the design patterns used (if any) and the anti-patterns present. Respond in JSON: {"patterns": ["pattern1"], "anti_patterns": ["anti-pattern1", "anti-pattern2"]}""",

            # Prompt 2: Spot Code Smells
            """Based on the anti-patterns {{output[-1].anti_patterns}}, list specific 'code smells' and technical debt risks. What will break if this scales? Respond in JSON: {"code_smells": ["smell1", "smell2"], "risks": ["risk1", "risk2"]}""",

            # Prompt 3: Propose Refactoring
            """Propose specific refactoring steps to fix the smells {{output[-1].code_smells}}. How would you make this cleaner and more testable? Respond in JSON: {"refactoring_steps": ["step1", "step2", "step3"]}""",

            # Prompt 4: Predict Maintenance Costs
            """If we DON'T refactor, predict the long-term maintenance costs. What specific bugs or headaches will this cause for future developers? Respond in JSON: {"maintenance_prediction": "description of future pain"}""",

            # Prompt 5: Generate Architecture Diagram Description
            """Describe a high-level architectural diagram of the IMPROVED state after your refactoring steps ({{output[-2].refactoring_steps}}). Use Mermaid.js syntax format if possible, or just a clear text description of components and data flow. Respond in JSON: {"architecture_diagram": "mermaid_or_text_description"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "architecture_prompts")
    results_file_base = os.path.join(output_dir, "architecture_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("code_architecture_critic", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        architecture_demo()
