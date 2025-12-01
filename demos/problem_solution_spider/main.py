# These lines at the top are like telling Python where to find its tools.
# 'import sys' and 'import os' help us work with the computer's files and settings.
import sys
import os

# This next part figures out where our main project folder is.
# It's like finding the main entrance to our project's "house."
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# This 'if' block makes sure Python looks in our main project folder first
# when we ask it to 'import' (bring in) tools.
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

# Now we're importing our special tools!
# 'MinimalChainable' is our main LEGO builder for prompts.
# 'build_models' helps set up our AI friends (the Gemini models).
# 'prompt' is the function that sends our message to the AI.
from chain import MinimalChainable # Our magic prompt chaining tool
from main import build_models, prompt # Tools from our main project file

# This is our Problem-Solution Spider adventure!
# A 'def' creates a function, which is like a recipe for the computer.
def problem_solution_spider_demo():
    # Let's tell everyone what we're doing!
    print("🚀 Running: Problem-Solution Spider Demo")

    # First, let's get our AI models ready.
    client, model_names = build_models()
    # We'll pick the first AI friend from the list to help us.
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # This is the problem we want the AI to help us solve.
    # Try changing this to a different problem you want to think about!
    # For example: "kids in my neighborhood don't have a safe place to play outside"
    # or "my backpack is always too messy and I can't find anything"
    problem_to_solve = "Students often forget their homework at home."

    # Let's print which problem we're tackling.
    print(f"Attempting to solve the problem: {problem_to_solve}\n")

    # This is the exciting part where we run our prompt chain!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' is like giving our AI starting information.
        context={"problem": problem_to_solve},
        # 'model' tells it which AI friend to talk to.
        model=model_info,
        # 'callable' is the function that actually sends the message to the AI.
        callable=prompt,
        # 'prompts' is a list of questions we'll ask the AI, one after another.
        prompts=[
            # Prompt 1: Define the problem clearly.
            # "{{problem}}" will be replaced with our chosen problem_to_solve.
            # We ask the AI to answer in JSON format.
            """Clearly define the problem: '{{problem}}' for a 5th-grade audience. What are the main issues involved? Respond in JSON like {"defined_problem": "clear definition and main issues"}""",

            # Prompt 2: List constraints.
            # "{{output[-1].defined_problem}}" uses the defined problem from the AI's last answer.
            """For the problem '{{output[-1].defined_problem}}', list 2-3 common constraints or limitations a 5th grader might face when trying to solve it (e.g., limited budget, school rules, not much time). Respond in JSON like {"constraints": ["constraint1", "constraint2", ...]}""",

            # Prompt 3: Brainstorm wild ideas.
            # "{{output[-2].defined_problem}}" uses the problem from 2 answers ago.
            # "{{output[-1].constraints}}" uses the constraints from the last answer.
            """Let's brainstorm! For the problem '{{output[-2].defined_problem}}' with constraints {{output[-1].constraints}}, suggest 3-4 wild and imaginative ideas to solve it. Don't worry if they seem silly or impossible right now. Respond in JSON like {"wild_ideas": [{"idea": "wild idea 1 description"}, ...]}""",

            # Prompt 4: Combine the best parts of wild ideas.
            # "{{output[-1].wild_ideas}}" uses the wild ideas from the AI's last answer.
            """Look at these wild ideas for '{{output[-3].defined_problem}}': {{output[-1].wild_ideas}}. Now, try to combine the best parts of 1-2 of these ideas to create a more practical, creative solution. Describe the combined solution. Respond in JSON like {"combined_solution": "description of combined solution"}""",

            # Prompt 5: Test the combined solution with a scenario.
            # "{{output[-1].combined_solution}}" uses the combined solution from the last answer.
            """Let's test the solution: '{{output[-1].combined_solution}}' for the problem '{{output[-4].defined_problem}}'. Describe a brief scenario where a 5th grader tries this solution. What happens? Does it work well? What could be improved? Respond in JSON like {"scenario_test": {"outcome": "description of what happens", "improvements_needed": "any improvements"}}"""
        ],
    )

    # Now we'll save our results to text files so we can look at them later.
    output_dir = os.path.dirname(__file__) # The folder where this script is.
    # We decide what to name our output files.
    prompts_file_base = os.path.join(output_dir, "problem_solution_spider_prompts")
    results_file_base = os.path.join(output_dir, "problem_solution_spider_results")

    # This line uses our tool to make a nice text file of all the prompts we sent.
    chained_prompts_text = MinimalChainable.to_delim_text_file(
        prompts_file_base,      # The name for the file
        context_filled_prompts  # The actual prompts we sent
    )
    # This line makes a nice text file of all the answers the AI gave us.
    chainable_result_text = MinimalChainable.to_delim_text_file(
        results_file_base,      # The name for this file
        result                  # The AI's answers
    )

    # Let's print everything to the screen so we can see it right away!
    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    # And tell the user where the files were saved.
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

# This special code block runs only when you run this file directly.
if __name__ == "__main__":
    # This part helps load our secret API key from a file named '.env'.
    # The API key is like a password to talk to AI models through OpenRouter.
    from dotenv import load_dotenv
    # We need to find the '.env' file, which is in our main project folder.
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path) # Load the secret key
    else:
        # If the file isn't there, print a friendly warning.
        print(f"Warning: .env file not found at {dotenv_path}. Make sure OPENROUTER_API_KEY is set in your environment.")

    # Check if we actually got the API key.
    if not os.getenv("OPENROUTER_API_KEY"):
        # If not, tell the user what to do.
        print("🚨 OPENROUTER_API_KEY not found. Please set it up in the .env file in the project root.")
    else:
        # If we have the key, then it's time to run our problem_solution_spider_demo recipe!
        problem_solution_spider_demo()