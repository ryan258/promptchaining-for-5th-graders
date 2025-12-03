#!/bin/bash
# Verify all demos run without immediate errors

echo "Starting verification of all demos..."
failed_demos=()

for demo in demos/*/main.py; do
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
    
    # Run for 5 seconds. If it exits with 0 or 124 (timeout), it's likely fine (started ok).
    # If it exits with 1 (error), it's broken.
    output=$($CMD 5s python3 "$demo" 2>&1)
    exit_code=$?
    
    # Check for common python errors in output even if exit code is masked by timeout
    if echo "$output" | grep -q "Traceback"; then
        echo "❌ FAILED: $demo"
        echo "$output" | head -n 20
        failed_demos+=("$demo")
    elif echo "$output" | grep -q "Error:"; then
        echo "❌ FAILED (Error detected): $demo"
        echo "$output" | head -n 20
        failed_demos+=("$demo")
    elif echo "$output" | grep -q "ModuleNotFoundError"; then
        echo "❌ FAILED (Import Error): $demo"
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
