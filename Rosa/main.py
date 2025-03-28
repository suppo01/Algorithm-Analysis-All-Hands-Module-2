"""This script identifies the test case with the highest coverage from a JSON file."""

from quick_sort import measure_sorting_time
from typing import List, Dict, Any


# Path to your test metrics file
file_path = '../data/newtryingToCompute.json'  # Updated again to new file

# Function to find the test case with the highest coverage
def find_highest_coverage_test_case(sorted_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Finds the test case with the highest coverage."""
    # Start with the first test case as the one with the highest coverage
    highest_coverage_test: Dict[str, Any] = sorted_tests[0]

    # Loop through all test cases to find the one with the largest coverage
    for test in sorted_tests:
        if test['coverage'] > highest_coverage_test['coverage']:
            highest_coverage_test = test  # Update the test case with the highest coverage

    return highest_coverage_test  # Return the test case with the largest coverage

# Add a blank line
print("\n🌟 Results 🌟")

# line for spacing
print()

# Measure running time and sort by coverage
sorted_tests_by_coverage: List[Dict[str, Any]] = measure_sorting_time(file_path, 'coverage')

# Find the test case with the highest coverage
highest_coverage_test_case: Dict[str, Any] = find_highest_coverage_test_case(sorted_tests_by_coverage)

# Print the test case with the highest coverage
print("\n🚀 Test Case with Highest Coverage:")
print(f"Test Name: {highest_coverage_test_case['name']}")
print(f"Coverage: {highest_coverage_test_case['coverage']}")

