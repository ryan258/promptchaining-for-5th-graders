# These lines at the top are like telling Python where to find its tools.
import sys
import os

# This next part figures out where our main project folder is.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# This 'if' block makes sure Python looks in our main project folder first for tools.
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

# Now we're importing our special tools!
# 'MinimalChainable' is our main LEGO builder for prompts.
# 'build_models' helps set up our AI friends.
# 'prompt' is the function that sends our message to the AI.
from chain import MinimalChainable # Our magic prompt chaining tool
from main import build_models, prompt # Tools from our main project file

# This is our Concept Simplifier recipe!
def concept_simplifier_demo():
    # Let's tell everyone what this demo does.
    print("🚀 Running: Concept Simplifier Demo")

    # Get our AI models ready to help.
    client, model_names = build_models()
    # We'll use the first AI friend in the list.
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # This is the tricky topic we want the AI to explain simply.
    # Try changing this to something else you're curious about!
    complex_topic = "Photosynthesis"
    # Show what topic we're working on.
    print(f"Simplifying Topic: {complex_topic}\n")

    # Time to run our prompt chain!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' gives the AI the starting topic.
        context={"topic": complex_topic},
        # Which AI friend to use.
        model=model_info,
        # The function to send messages to the AI.
        callable=prompt,
        # Our list of step-by-step questions for the AI.
        prompts=[
            # Prompt 1: Break the topic into small pieces.
            # "{{topic}}" will be replaced with "Photosynthesis".
            # We ask for the answer in JSON format (like a dictionary).
            """Break the complex topic '{{topic}}' into 3-4 main parts a 5th grader can understand. Respond in JSON: {"parts": ["part1 explanation", "part2 explanation", ...]}""",

            # Prompt 2: Find simple comparisons (analogies).
            # "{{output[-1].parts}}" uses the 'parts' from the AI's last answer.
            """For the topic '{{topic}}' and its parts {{output[-1].parts}}, find a simple analogy for each part to help a 5th grader understand. Respond in JSON: {"analogies": [{"part": "original part1", "analogy": "analogy1"}, ...]}""",

            # Prompt 3: Give examples for those analogies.
            # "{{output[-1].analogies}}" uses the 'analogies' from the AI's last answer.
            """Using the analogies from {{output[-1].analogies}} for '{{topic}}', provide a simple example for each to test understanding. Respond in JSON: {"examples": [{"analogy_for_part": "analogy1", "example": "example1"}, ...]}""",

            # Prompt 4: Create a short teaching story.
            # This prompt uses answers from three previous steps!
            # "{{output[-3].parts}}" gets the parts from 3 answers ago.
            # "{{output[-2].analogies}}" gets the analogies from 2 answers ago.
            # "{{output[-1].examples}}" gets the examples from the last answer.
            """Now, create a very short teaching story (3-5 sentences) for a 5th grader that explains '{{topic}}' using the main parts, analogies, and examples from {{output[-3].parts}}, {{output[-2].analogies}}, and {{output[-1].examples}}. Make it engaging! Respond in JSON: {"story": "your teaching story"}"""
        ],
    )

    # Let's save the prompts we sent and the AI's answers into files.
    output_dir = os.path.dirname(__file__) # The folder where this script lives.
    # Names for our output files.
    prompts_file_base = os.path.join(output_dir, "concept_simplifier_prompts")
    results_file_base = os.path.join(output_dir, "concept_simplifier_results")

    # Make a nice text file of the prompts.
    chained_prompts_text = MinimalChainable.to_delim_text_file(
        prompts_file_base,
        context_filled_prompts
    )
    # Make a nice text file of the AI's answers.
    chainable_result_text = MinimalChainable.to_delim_text_file(
        results_file_base,
        result
    )

    # Show the prompts and answers on the screen.
    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    # Tell the user where the files are saved.
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    # Also log to markdown for history
    log_file = MinimalChainable.log_to_markdown("concept_simplifier", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")


# This special code runs if you start this Python file directly.
if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        concept_simplifier_demo()