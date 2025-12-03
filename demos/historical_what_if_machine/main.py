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

# This is our Historical What-If Machine adventure!
# A 'def' creates a function, which is like a recipe for the computer.
def historical_what_if_demo():
    # Let's tell everyone what we're doing!
    print("🚀 Running: Historical What-If Machine Demo")

    # First, let's get our AI models ready.
    client, model_names = build_models()
    # We'll pick the first AI friend from the list to help us.
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # This is the historical event we want to explore.
    # Try changing this! Examples: "The first moon landing", "The discovery of fire",
    # "The invention of the printing press"
    historical_event = "The Titanic Sinking"
    # This is the one thing we'll change about the event.
    # Example: "What if the Titanic had more lifeboats?"
    # or "What if the Titanic hit the iceberg at a different angle?"
    changed_variable = "What if the Titanic received the iceberg warnings and slowed down significantly?"

    # Let's print what historical "what-if" we're exploring.
    print(f"Exploring a 'What If' scenario for: {historical_event}")
    print(f"The change is: {changed_variable}\n")

    # This is the exciting part where we run our prompt chain!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' is like giving our AI starting information.
        context={"event": historical_event, "change": changed_variable},
        # 'model' tells it which AI friend to talk to.
        model=model_info,
        # 'callable' is the function that actually sends the message to the AI.
        callable=prompt,
        # 'prompts' is a list of questions we'll ask the AI, one after another.
        prompts=[
            # Prompt 1: Briefly describe the original historical event.
            "Briefly describe the historical event: '{{event}}' for a 5th grader. Respond in JSON like {\"original_event_summary\": \"summary\"}",

            # Prompt 2: Predict immediate consequences of the change.
            # "{{change}}" is our "what-if" question.
            # "{{output[-1].original_event_summary}}" uses the summary from the AI's last answer.
            "Consider the event '{{event}}' ({{output[-1].original_event_summary}}). If we change one thing: '{{change}}', what are 1-2 immediate consequences that might happen right away? Respond in JSON like {\"immediate_consequences\": [\"consequence1\", \"consequence2\"]}",

            # Prompt 3: Trace short-term ripple effects (1-5 years later).
            # "{{output[-1].immediate_consequences}}" uses the consequences from the last answer.
            "Based on these immediate consequences for '{{event}}' if '{{change}}' happened ({{output[-1].immediate_consequences}}), what are 2-3 short-term ripple effects that might be seen 1 to 5 years later? Respond in JSON like {\"short_term_ripple_effects\": [\"effect1\", \"effect2\"]}",

            # Prompt 4: Trace long-term ripple effects (20+ years later).
            # "{{output[-1].short_term_ripple_effects}}" uses the short-term effects from the last answer.
            "Thinking about the short-term ripple effects ({{output[-1].short_term_ripple_effects}}) from our '{{change}}' to '{{event}}', what could be 1-2 significant long-term ripple effects seen 20 or more years later? Respond in JSON like {\"long_term_ripple_effects\": [\"long_effect1\", \"long_effect2\"]}",

            # Prompt 5: What can we learn from this "what-if" scenario?
            # This prompt uses information from several previous steps!
            "Considering this entire 'what-if' scenario for '{{event}}' where '{{change}}' led to immediate consequences {{output[-3].immediate_consequences}}, short-term effects {{output[-2].short_term_ripple_effects}}, and long-term effects {{output[-1].long_term_ripple_effects}}, what's one important lesson this teaches us about what really mattered in the original historical event? Respond in JSON like {\"lesson_learned\": \"the important lesson\"}"
        ],
    )

    # Now we'll save our results to text files so we can look at them later.
    output_dir = os.path.dirname(__file__) # The folder where this script is.
    # We decide what to name our output files.
    prompts_file_base = os.path.join(output_dir, "historical_what_if_prompts")
    results_file_base = os.path.join(output_dir, "historical_what_if_results")

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

    # Log the run to markdown
    log_file = MinimalChainable.log_to_markdown("historical_what_if_machine", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

# This special code block runs only when you run this file directly.
if __name__ == "__main__":
    # This part helps load our secret API key from a file named '.env'.
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
        # If we have the key, then it's time to run our historical_what_if_demo recipe!
        historical_what_if_demo()