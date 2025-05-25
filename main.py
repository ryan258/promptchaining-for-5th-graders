# main.py - Using the Prompt Chain Magic
# This file shows how to use our prompt chaining system
# Think of this as the cookbook that shows you how to cook with our tools

# import os # Helps us read secret keys from the computer
from typing import List, Dict, Union # Tells Python what types of data we expect
# from dotenv import load_dotenv # Helps us load secret keys from a file
from chain import MinimalChainable, FusionChain # Our magic prompt chaining tools
import google.generativeai as genai # Google's library that talks to Gemini AI models
import json # Helps us work with data that looks like {"key": "value"}

from dotenv import load_dotenv # Make sure this import is there
import os # Make sure this import is there

def build_models():
    """
    This function sets up our AI models so we can talk to them.
    # ... (rest of your docstring)
    """


    print("Attempting to load .env file...") # DEBUG
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    print(f"Loaded GOOGLE_API_KEY: {GOOGLE_API_KEY[:10]}..." if GOOGLE_API_KEY else "GOOGLE_API_KEY is NOT loaded") # DEBUG line - shows first 10 chars

    if not GOOGLE_API_KEY:
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
        
    # Check if we actually got the key
    if not GOOGLE_API_KEY:
        raise ValueError(
            "🔑 Missing API key! Please:\n"
            "   1. Copy .env.example to .env\n"
            "   2. Get your key from https://makersuite.google.com/app/apikey\n"
            "   3. Add it to your .env file as GOOGLE_API_KEY=your_key_here"
        )
    
    # Tell Google's library to use our secret key
    genai.configure(api_key=GOOGLE_API_KEY)

    # Set up our three Gemini model friends
    # They're all fast and affordable - perfect for learning!
    
    # Gemini 2.5 Flash - newest stable model, fast and cost-effective
    # Let's try "gemini-1.5-flash-latest" or just "gemini-1.5-flash"
    gemini_2_5_flash_model = genai.GenerativeModel("gemini-1.5-flash-latest") # TRY THIS FIRST

    # Gemini 2.5 Pro - more powerful for complex reasoning
    # Let's try "gemini-1.5-pro-latest" or "gemini-pro" (which is 1.0)
    gemini_2_5_pro_model = genai.GenerativeModel("gemini-1.5-pro-latest") # TRY THIS
    
    # Gemini 1.0 Pro - reliable and well-tested
    gemini_1_0_pro_model = genai.GenerativeModel("gemini-pro") # This one is likely fine


    # Return all three models so we can use them later
    return [gemini_2_5_flash_model, gemini_2_5_pro_model, gemini_1_0_pro_model]


def prompt(model: genai.GenerativeModel, prompt: str):
    """
    This function sends a message to a Gemini AI model and gets back an answer.
    
    It's like sending a text message to your smart friend and waiting
    for them to text you back with an answer.
    """
    
    try:
        # Configure the model settings
        # Temperature 0.5 means "be creative, but not too crazy"
        generation_config = genai.types.GenerationConfig(
            temperature=0.5, # How creative should the AI be? (0 = boring, 1 = very creative)
            max_output_tokens=1000, # Maximum length of response
        )
        
        # Send the prompt to the model and get a response
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Get just the text part of the response
        return response.text
        
    except Exception as e:
        # If something goes wrong, give a helpful message instead of a scary error
        return f"Oops! Something went wrong talking to the AI: {str(e)}\nCheck your API key in the .env file!"


def prompt_chainable_poc():
    """
    This function shows how to use MinimalChainable to chain prompts together.
    
    POC means "Proof of Concept" - we're proving that our idea works!
    
    We're going to:
    1. Ask AI to create a blog post title about AI Agents
    2. Ask AI to create a hook for that title  
    3. Ask AI to write the first paragraph using the title and hook
    
    Each step builds on the previous one, like building with blocks!
    """
    
    # Get our AI models
    all_models = build_models()
    # Select the gemini-2.5-flash model for this PoC
    # The first model returned by build_models() is gemini_2_5_flash_model
    selected_model = all_models[0] 

    # Run our prompt chain!
    # This returns two things:
    # - result: the answers from each prompt
    # - context_filled_prompts: the actual prompts we sent (with variables filled in)
    result, context_filled_prompts = MinimalChainable.run(
        
        # Our starting context - this is like our bag of ingredients
        context={"topic": "AI Agents"},
        
        # Which AI model to use - now explicitly using the selected Gemini model
        model=selected_model, # Changed from gemini_flash_new / sonnet_3_5_model
        
        # The function that sends prompts to the AI
        callable=prompt,
        
        # Our chain of prompts - each one builds on the previous ones!
        prompts=[
            # PROMPT #1: Create a blog title
            # {{topic}} gets replaced with "AI Agents"
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {'title': '<title>'}",
            
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


def fusion_chain_poc():
    """
    This function shows how to use FusionChain to make AI models compete!
    
    Instead of using just one AI model, we use three different ones
    and make them all answer the same questions. Then we pick the best answer!
    
    It's like asking three different friends the same question and
    choosing who gave the best response.
    """
    
    # Get all three of our Gemini AI models
    all_gemini_models = build_models() # Renamed for clarity

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
        
        # Use all three Gemini models - they'll compete!
        models=all_gemini_models, # Changed from 'models'
        
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
        get_model_name=lambda model: model.model_name,
    )

    # Convert our result to a dictionary so we can save it as JSON
    result_dump = result.model_dump() # Pydantic v2 uses model_dump() instead of dict()

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
        all_models = build_models()
        test_model = all_models[0] # Use the first model (gemini_2_5_flash_model)
        
        # Send a simple test message
        test_response = prompt(test_model, "Say 'Hello, young builder!' if you can hear me.")
        
        print("✅ Success! Your AI is ready to chain prompts!")
        print(f"🤖 AI says: {test_response}")
        return True
        
    except Exception as e:
        print("❌ Setup test failed!")
        print(f"🐛 Error: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("   1. Check that you have a .env file with your GOOGLE_API_KEY")
        print("   2. Make sure you copied your key correctly from Google AI Studio")
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

    # Uncomment the next line if you want to see fusion chaining too!
    # (We comment it out because it uses more AI calls and potentially costs more)
    # print("\n" + "="*60)
    # print("🔥 Now for the FusionChain Competition!")
    # print("="*60)
    # fusion_chain_poc()


# This special code means "only run main() if this file is being run directly"
# It's like saying "if someone double-clicks this file, run the main function"
if __name__ == "__main__":
    main()