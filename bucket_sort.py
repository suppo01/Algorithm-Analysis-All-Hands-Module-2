"""This script identifies the test case with the highest coverage from a JSON file using bucket sort."""

import json
import os
from typing import List, Dict, Any

# Function to perform bucket sort on test cases based on a given attribute
def bucket_sort(data: List[Dict[str, Any]], attribute: str) -> List[Dict[str, Any]]:
    """Sort a list of dictionaries using bucket sort based on a given attribute."""
    max_value = max(item[attribute] for item in data)  # Find the maximum value of the attribute
    buckets = [[] for _ in range(int(max_value) + 1)]  # Create buckets

    for item in data:  # Place each item in the appropriate bucket
        buckets[int(item[attribute])].append(item)

    sorted_data = []  # Concatenate all buckets into a sorted list
    for bucket in buckets:
        sorted_data.extend(bucket)

    return sorted_data  # Return the sorted list

# Function to load data from a JSON file
def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file."""
    if not os.path.exists(file_path):  # Check if the file exists
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data  # Return the loaded data

# Function to find the test case with the highest coverage
def find_highest_coverage_test_case(sorted_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Finds the test case with the highest coverage."""
    highest_coverage_test: Dict[str, Any] = sorted_tests[0]  # Start with the first test case
    for test in sorted_tests:  # Loop through all test cases
        if test['coverage'] > highest_coverage_test['coverage']:
            highest_coverage_test = test  # Update the test case with the highest coverage
    return highest_coverage_test  # Return the test case with the largest coverage

# Main function to execute the script
def main():
    file_path = 'data/newtryingToCompute.json'  # Path to your test metrics file

    # Debugging: Print the absolute path being used
    print(f"Looking for file at: {os.path.abspath(file_path)}")

    try:
        data = load_data(file_path)  # Load the test metrics data
    except FileNotFoundError as e:
        print(e)
        return

    sorted_tests_by_coverage: List[Dict[str, Any]] = bucket_sort(data, 'coverage')  # Sort by coverage
    highest_coverage_test_case: Dict[str, Any] = find_highest_coverage_test_case(sorted_tests_by_coverage)  # Find the highest coverage

    # Print the results
    print("\n🌟 Results 🌟")
    print("\n🚀 Test Case with Highest Coverage:")
    print(f"Test Name: {highest_coverage_test_case['name']}")
    print(f"Coverage: {highest_coverage_test_case['coverage']}")

# Entry point of the script
if __name__ == "__main__":
    main()