#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate  # Use venv/bin/activate if on Linux/MacOS

# Check if activation was successful
if [[ $? -ne 0 ]]; then
    echo "Failed to activate the virtual environment."
    exit 1
fi

echo "Virtual environment activated."

# Run the test suite using pytest
pytest test_app.py

# Capture the exit code from pytest
TEST_EXIT_CODE=$?

# Deactivate the virtual environment
deactivate

# Exit with pytest's exit code
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Some tests failed. Check the output above for details."
    exit 1
fi
