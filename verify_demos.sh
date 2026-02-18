#!/bin/bash
# Verify all demos run without immediate errors

echo "Starting verification of all demos..."
failed_demos=()

shopt -s nullglob
demo_files=(demos/*.py)

if [ ${#demo_files[@]} -eq 0 ]; then
    echo "🚨 No demo files found in demos/"
    exit 1
fi

for demo in "${demo_files[@]}"; do
    echo "--------------------------------------------------"
    echo "Testing $demo..."
    
    # Run the demo with a timeout to prevent hanging
    # We only care if it starts successfully, so we capture stderr/stdout
    # and look for python errors.
    # We use 'gtimeout' if available (common on mac with coreutils), else 'timeout'
    if command -v gtimeout &> /dev/null; then
        CMD="gtimeout"
    else
        CMD="timeout"
    fi
    
    # Feed input for interactive demos and run with timeout.
    # Exit 124 means timeout (acceptable: demo started and kept running).
    if [ "$(basename "$demo")" = "ms_blog_demo.py" ]; then
        output=$(printf "0\n" | $CMD 5s python3 "$demo" 2>&1)
    else
        output=$(yes "" | $CMD 5s python3 "$demo" 2>&1)
    fi
    exit_code=$?

    # Check for common Python errors in output.
    if echo "$output" | grep -q "Traceback"; then
        echo "❌ FAILED: $demo"
        echo "$output" | head -n 20
        failed_demos+=("$demo")
    elif echo "$output" | grep -q "ModuleNotFoundError"; then
        echo "❌ FAILED (Import Error): $demo"
        echo "$output" | head -n 20
        failed_demos+=("$demo")
    elif [ "$exit_code" -ne 0 ] && [ "$exit_code" -ne 124 ]; then
        echo "❌ FAILED (Exit $exit_code): $demo"
        echo "$output" | head -n 20
        failed_demos+=("$demo")
    else
        echo "✅ PASSED: $demo"
    fi
done

echo "--------------------------------------------------"
if [ ${#failed_demos[@]} -eq 0 ]; then
    echo "🎉 All demos passed verification!"
    exit 0
else
    echo "🚨 The following demos failed:"
    for demo in "${failed_demos[@]}"; do
        echo "- $demo"
    done
    exit 1
fi
