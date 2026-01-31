# main.py - Using the Prompt Chain Magic
# This file shows how to use our prompt chaining system
# Think of this as the cookbook that shows you how to cook with our tools

from typing import List, Dict, Union, Tuple
import json  # Helps us work with data that looks like {"key": "value"}
import os  # Helps us read secret keys from the computer

from .chain import MinimalChainable, FusionChain
from .llm_client import build_models, prompt


def prompt_chainable_poc():
    """
    POC means "Proof of Concept" - we're proving that our idea works!
    
    We're going to:
    1. Ask AI to create a blog post title about AI Agents
    2. Ask AI to create a hook for that title  
    3. Ask AI to write the first paragraph using the title and hook
    
    Each step builds on the previous one, like building with blocks!
    """
    
    # Get our AI models
    client, model_names = build_models()
    # Select the first model for this PoC
    selected_model_name = model_names[0] 
    
    # We pass both the client and the model name as a tuple
    model_info = (client, selected_model_name)

    # Run our prompt chain!
    # This returns two things:
    # - result: the answers from each prompt
    # - context_filled_prompts: the actual prompts we sent (with variables filled in)
    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        
        # Our starting context - this is like our bag of ingredients
        context={"topic": "AI Agents"},
        
        # Which AI model to use - now passing the tuple
        model=model_info,
        
        # The function that sends prompts to the AI
        callable=prompt,
        
        # Our chain of prompts - each one builds on the previous ones!
        prompts=[
            # PROMPT #1: Create a blog title
            # {{topic}} gets replaced with "AI Agents"
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {\"title\": \"<title>\"}",
            
            # PROMPT #2: Create a hook for that title
            # {{output[-1].title}} gets the title from the previous response
            "Generate one hook for the blog post title: {{output[-1].title}}",
            
            # PROMPT #3: Write the first paragraph
            # {{output[-2].title}} gets the title from 2 prompts ago
            # {{output[-1]}} gets the hook from the last prompt
            """Based on the BLOG_TITLE and BLOG_HOOK, generate the first paragraph of the blog post.
BLOG_TITLE:
{{output[-2].title}}
BLOG_HOOK:
{{output[-1]}}""",
        ],
        return_usage=True,
    )

    # Save our results to text files so we can see what happened
    # This creates two files:
    # 1. A file showing the prompts we actually sent
    # 2. A file showing the responses we got back
    
    chained_prompts = MinimalChainable.to_delim_text_file(
        "poc_context_filled_prompts", # Name of the file
        context_filled_prompts # The prompts with variables filled in
    )
    
    chainable_result = MinimalChainable.to_delim_text_file(
        "poc_prompt_results", # Name of the file  
        result # The AI responses
    )

    # Print everything to the screen so we can see what happened
    print(f"\n\n📖 Prompts~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n\n{chained_prompts}")
    print(f"\n\n📊 Results~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n\n{chainable_result}")

    # Log to markdown for cost reporting
    MinimalChainable.log_to_markdown("poc_demo", context_filled_prompts, result, usage_stats)


def fusion_chain_poc():
    """
    This function shows how to use FusionChain to make AI models compete!
    
    Instead of using just one AI model, we use three different ones
    and make them all answer the same questions. Then we pick the best answer!
    
    It's like asking three different friends the same question and
    choosing who gave the best response.
    """
    
    # Get our AI models
    client, model_names = build_models()
    
    # Create a list of (client, model_name) tuples for all models
    all_models = [(client, name) for name in model_names]

    def evaluator(outputs: List[str]) -> tuple[str, List[float]]:
        """
        This function decides which AI model did the best job.
        
        Our simple strategy: the longest answer wins!
        (In real life, you might use more complex judging)
        """
        
        # Count how many characters each output has
        scores = [len(output) for output in outputs]
        
        # Find the highest score
        max_score = max(scores) if scores else 0 # Handle case where outputs might be empty
        
        # Turn scores into percentages (0 to 1)
        # Avoid division by zero if max_score is 0
        normalized_scores = [(score / max_score) if max_score > 0 else 0 for score in scores] 
        
        # The output with the highest score wins
        if not outputs: # Handle empty outputs list
            return "No output to evaluate.", []

        top_response = outputs[scores.index(max_score)] if scores else "No output to evaluate."
        
        return top_response, normalized_scores

    # Run the fusion chain - this is where the magic happens!
    result = FusionChain.run(
        
        # Same context as before
        context={"topic": "AI Agents"},
        
        # Use all three models - they'll compete!
        models=all_models,
        
        # Function to send prompts
        callable=prompt,
        
        # Same prompt chain as before
        prompts=[
            # PROMPT #1: Create a blog title
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {'title': '<title>'}",
            
            # PROMPT #2: Create a hook
            "Generate one hook for the blog post title: {{output[-1].title}}",
            
            # PROMPT #3: Write first paragraph
            """Based on the BLOG_TITLE and BLOG_HOOK, generate the first paragraph of the blog post.
BLOG_TITLE:
{{output[-2].title}}
BLOG_HOOK:
{{output[-1]}}""",
        ],
        
        # Our judging function
        evaluator=evaluator,
        
        # Function to get model names for the report
        get_model_name=lambda model_info: model_info[1],
    )

    # Convert our result to a dictionary so we can save it as JSON
    try:
        # Try model_dump first (Pydantic v2)
        result_dump = result.model_dump()
    except Exception as e:
        print(f"⚠️ model_dump failed: {e}")
        try:
            # Try dict (Pydantic v1 or fallback)
            result_dump = result.dict()
        except Exception as e2:
            print(f"⚠️ dict failed: {e2}")
            # Manual fallback
            result_dump = {
                "top_response": result.top_response,
                "all_prompt_responses": result.all_prompt_responses,
                "all_context_filled_prompts": result.all_context_filled_prompts,
                "performance_scores": result.performance_scores,
                "model_names": result.model_names,
                "all_usage_stats": result.all_usage_stats
            }

    # Print the results to the screen
    print("\n\n📊 FusionChain Results~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(json.dumps(result_dump, indent=4)) # Pretty print the JSON

    # Save the complete results to a JSON file
    with open("poc_fusion_chain_result.json", "w") as json_file:
        json.dump(result_dump, json_file, indent=4)


def verify_setup():
    """
    This function helps you test that everything is working correctly.
    
    It's like checking if your car starts before going on a road trip.
    We'll try to connect to the AI and get a simple response.
    """
    
    print("🔧 Testing your AI setup...")
    
    try:
        # Try to build our models and use the first one for testing
        client, model_names = build_models()
        test_model_info = (client, model_names[0]) # Use the first model
        
        # Send a simple test message
        test_response = prompt(test_model_info, "Say 'Hello, young builder!' if you can hear me.")

        # Handle both tuple and string responses
        if isinstance(test_response, tuple):
            content, usage = test_response
        else:
            content, usage = test_response, None
        
        if usage is None or (isinstance(content, str) and content.startswith("Error:")):
            raise Exception(f"Prompt failed: {content}")

        print("✅ Success! Your AI is ready to chain prompts!")
        print(f"🤖 AI says: {content}")
        return True
        
    except Exception as e:
        print("❌ Setup test failed!")
        print(f"🐛 Error: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("   1. Check that you have a .env file with your OPENROUTER_API_KEY")
        print("   2. Make sure you copied your key correctly from OpenRouter")
        print("   3. Verify you have internet connection")
        print("   4. Try running: pip install -r requirements.txt")
        return False


def main():
    """
    This is the main function that runs when we start the program.
    
    It's like the conductor of an orchestra - it decides which
    pieces of music (functions) to play and in what order.
    """
    
    # First, let's make sure everything is working
    if not verify_setup():
        print("\n🚫 Please fix the setup issues above before continuing.")
        return # Exit if setup fails
    
    print("\n" + "="*60)
    print("🎪 Welcome to the Prompt Chaining Carnival!")
    print("="*60)
    
    # Show how basic prompt chaining works
    prompt_chainable_poc()

    # FusionChain is opt-in because it uses more AI calls (higher cost)
    run_fusion = os.getenv("RUN_FUSION_CHAIN", "").lower() in ("1", "true", "yes")
    if run_fusion:
        print("\n" + "="*60)
        print("🔥 Now for the FusionChain Competition!")
        print("="*60)
        fusion_chain_poc()
    else:
        print("\n💡 Skipping FusionChain by default to save cost. Set RUN_FUSION_CHAIN=1 to enable.")


# This special code means "only run main() if this file is being run directly"
# It's like saying "if someone double-clicks this file, run the main function"
if __name__ == "__main__":
    main()
