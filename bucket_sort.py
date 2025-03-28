"""This script identifies the test case with the highest coverage from a JSON file using bucket sort."""

import json
from typing import List, Dict, Any

# Function to perform bucket sort on test cases based on a given attribute
def bucket_sort(data: List[Dict[str, Any]], attribute: str) -> List[Dict[str, Any]]:
    """Sort a list of dictionaries using bucket sort based on a given attribute."""
    # Find the maximum value of the attribute
    max_value = max(item[attribute] for item in data)
    # Create buckets (one for each integer value up to max_value)
    buckets = [[] for _ in range(int(max_value) + 1)]

    # Place each item in the appropriate bucket
    for item in data:
        buckets[int(item[attribute])].append(item)

    # Concatenate all buckets into a sorted list
    sorted_data = []
    for bucket in buckets:
        sorted_data.extend(bucket)

    return sorted_data  # Return the sorted list

# Function to load data from a JSON file
def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data  # Return the loaded data

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

# Main function to execute the script
def main():
    # Path to your test metrics file
    file_path = '../data/newtryingToCompute.json'  # Updated again to new file

    # Load the test metrics data
    data = load_data(file_path)

    # Sort the test cases by coverage using bucket sort
    sorted_tests_by_coverage: List[Dict[str, Any]] = bucket_sort(data, 'coverage')

    # Find the test case with the highest coverage
    highest_coverage_test_case: Dict[str, Any] = find_highest_coverage_test_case(sorted_tests_by_coverage)

    # Print the results
    print("\n🌟 Results 🌟")
    print("\n🚀 Test Case with Highest Coverage:")
    print(f"Test Name: {highest_coverage_test_case['name']}")
    print(f"Coverage: {highest_coverage_test_case['coverage']}")

# Entry point of the script
if __name__ == "__main__":
    main()