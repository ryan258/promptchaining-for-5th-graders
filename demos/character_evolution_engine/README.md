# Demo: The Character Evolution Engine

This demo creates characters that change and grow through their stories.

**Chain:**

1.  Basic character
2.  Give them a flaw
3.  Create a challenge
4.  Show growth
5.  Design new adventure

## How to Run

1.  Navigate to the `promptchaining-for-5th-graders` directory.
2.  Ensure your `.env` file is set up with your `GOOGLE_API_KEY`.
3.  Run the demo:
    ```bash
    python demos/character_evolution_engine/main.py
    ```

## Expected Output

The script will output a short story where a character evolves, including their initial description, a flaw, a challenge, how they grew, and a new adventure. Results are saved to `demos/character_evolution_engine/character_evolution_prompts.txt` and `demos/character_evolution_engine/character_evolution_results.txt`.
