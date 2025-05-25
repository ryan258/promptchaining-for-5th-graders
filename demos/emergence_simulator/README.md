# Demo: The Emergence Simulator 🐜🐦🐠

This demo shows how simple rules can lead to amazing and complex group behaviors, like how ants build colonies, birds flock, or fish school!

**Chain:**

1.  **Simple rules**: Start with 2-3 very simple rules for an individual "agent" (like a single ant, bird, or even a dot on a screen).
2.  **Individual behaviors**: Based on these rules, what would one agent do by itself?
3.  **Group interactions**: What happens when many agents, all following the same simple rules, start to interact with each other and their environment?
4.  **Emergent patterns**: What surprising or complex group behavior (pattern) "emerges" from all these simple interactions?
5.  **Real-world examples**: Can you think of examples in nature or real life where similar simple rules lead to complex group patterns?

**Real magic:** You understand how complexity emerges from simplicity! It's like seeing how a few simple LEGO bricks can be used to build a giant, detailed castle.

## How to Run

1.  Make sure you're in the main `promptchaining-for-5th-graders` folder in your terminal.
2.  Check that your `.env` file is ready with your `GOOGLE_API_KEY`.
3.  Run the demo with this command:
    ```bash
    python demos/emergence_simulator/main.py
    ```

## Expected Output

The script will use the AI to explore how simple rules can lead to complex behaviors. You'll see the AI define rules, predict individual and group actions, identify emergent patterns, and link them to real-world examples. The full simulation will also be saved into two files in the `demos/emergence_simulator/` folder:

- `emergence_simulator_prompts.txt` (all the questions we asked the AI)
- `emergence_simulator_results.txt` (all the AI's answers)
