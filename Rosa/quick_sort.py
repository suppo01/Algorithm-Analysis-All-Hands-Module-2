import json # Import the JSON module to handle JSON file operations
import time # Import the time module to measure execution time
import random  # Import random for selecting a random pivot in QuickSort
from typing import List, Dict, Any

def quicksort(arr: List[Any]) -> List[Any]:
    """Sorts an array using the QuickSort algorithm with a random pivot."""
    if len(arr) <= 1: # Base case if the array has 1 or no elements, it's already sorted
        return arr
    else:
        pivot = random.choice(arr)  # Select a random pivot element from the array
        left = [x for x in arr if x < pivot]  # Elements less than the pivot
        right = [x for x in arr if x > pivot]  # Elements greater than the pivot
        # Recursively sort the left and right partitions and combine them with the pivot
        return quicksort(left) + [pivot] + quicksort(right)



def quicksort_tests(tests: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    """Sorts the list of tests based on the specified key, handling both numbers and dictionaries."""
    if len(tests) <= 1: # Base case if the list has 1 or no elements, it is already sorted
        return tests
    else:
        pivot = tests[0] # Select the first dictionary in the list as the pivot
        pivot_value = pivot[key] # Get the value of the pivot for the specified key

        # If sorting by 'coverage', extract a single numerical value (sum of all coverage metrics)
        if isinstance(pivot_value, dict):
            pivot_value = sum(pivot_value.values())  # Convert dictionary to a single number

        # Create a list of dictionaries where the key's value is less than or equal to the pivot's value
        left = [test for test in tests[1:] if (sum(test[key].values()) if isinstance(test[key], dict) else test[key]) <= pivot_value]
        # Create a list of dictionaries where the key's value is greater than the pivot's value
        right = [test for test in tests[1:] if (sum(test[key].values()) if isinstance(test[key], dict) else test[key]) > pivot_value]

        # Recursively sort the left and right partitions and combine them with the pivot
        return quicksort_tests(left, key) + [pivot] + quicksort_tests(right, key)



def load_and_sort_metrics(file_path: str, sort_key: str) -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'r') as f: # Open the JSON file in read mode
            test_metrics = json.load(f) # Load the JSON data into a Python list
    except FileNotFoundError: # Handle the case where the file does not exist
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError: # Handle the case where the JSON file is invalid
        print(f"Invalid JSON format in file: {file_path}")
        return []

    # Check if the specified key exists in all test metrics
    if not all(sort_key in test for test in test_metrics):
        print(f"Key '{sort_key}' not found in all test metrics.")
        return []

    # Debug: Print the loaded data to see if the coverage is present
    # print(test_metrics)  # Check if coverage exists

    # Sort the test metrics using the QuickSort algorithm
    sorted_tests = quicksort_tests(test_metrics, sort_key)
    return sorted_tests


# This is called in main.py to benchmark
def measure_sorting_time(file_path: str, sort_key: str) -> List[Dict[str, Any]]:
    """
    Measures the time it takes to load and sort the metrics from a JSON file."""
    start_time = time.time()  # Record the start time
    sorted_tests = load_and_sort_metrics(file_path, sort_key) # Load and sort the metrics
    end_time = time.time() # Record the end time

    # Print the time taken to sort the metrics
    print(f"Sorting by {sort_key} took {end_time - start_time} seconds.")

    return sorted_tests # Return the sorted metrics
