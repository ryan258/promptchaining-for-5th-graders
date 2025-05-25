# Demo: The Subject Connector

This demo takes any two school subjects and finds surprising connections between them.

**Chain:**

1.  Subject A
2.  Subject B
3.  Find 3 connections
4.  Explain why they matter
5.  Design a project using both

## How to Run

1.  Navigate to the `promptchaining-for-5th-graders` directory.
2.  Ensure your `.env` file is set up with your `GOOGLE_API_KEY` as described in `GETTING_STARTED.md`.
3.  Run the demo:
    ```bash
    python demos/subject_connector/main.py
    ```

## Expected Output

The script will print the series of prompts sent to the AI and the AI's responses, culminating in a project idea that combines the two subjects. The results will also be saved to `demos/subject_connector/subject_connector_prompts.txt` and `demos/subject_connector/subject_connector_results.txt`.
