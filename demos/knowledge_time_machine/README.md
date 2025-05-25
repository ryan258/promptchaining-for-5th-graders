# Demo: The Knowledge Time Machine 🕰️🔬

This demo takes a modern concept (like a smartphone or the internet) and traces its journey through history, then peeks into its possible future!

**Chain:**

1.  Modern concept
2.  Historical origins (How did it start? What were the very first ideas?)
3.  Key evolution points (What important changes or discoveries happened along the way?)
4.  Current state (What is it like today?)
5.  Future possibilities (What might it become in the future? Wild ideas welcome!)

**Real magic:** You'll see how ideas build on each other over time and how today's inventions are part of a long story. It helps you understand that you can be part of that story too!

## How to Run

1.  Make sure you're in the main `promptchaining-for-5th-graders` folder in your terminal.
2.  Check that your `.env` file is ready with your `GOOGLE_API_KEY`.
3.  Run the demo with this command:
    ```bash
    python demos/knowledge_time_machine/main.py
    ```

## Expected Output

The script will print out the AI's step-by-step exploration of the chosen concept's history and future. You'll see how the AI answers each part of the chain. The full conversation will also be saved into two files in the `demos/knowledge_time_machine/` folder:

- `knowledge_time_machine_prompts.txt` (all the questions we asked the AI)
- `knowledge_time_machine_results.txt` (all the AI's answers)
