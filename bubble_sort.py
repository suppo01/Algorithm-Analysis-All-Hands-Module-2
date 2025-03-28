import functools
import sys
import time
import json
from typing import List, Dict
import argparse

def bubble_sort(data: List[Dict], attribute: str) -> List[Dict]:
    """Sort a list of dictionaries using the bubble sort algorithm based on a given attribute."""
    n = len(data)  # grabs the number of elements in the list
    for i in range(n):  # loop through all elements in the list
        for j in range(0, n - i - 1):  # loop through all elements in the list from 0 to n-i-1
            # Switch if the element found is greater than the next element
            if data[j][attribute] > data[j + 1][attribute]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

def load_data(file_path: str) -> List[Dict]:
    """Load data from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    parser = argparse.ArgumentParser(description="Sort a list of test metrics using bubble sort.")
    parser.add_argument("attribute", type=str, help="the attribute to sort by")
    parser.add_argument("--best", choices=["first", "last"], default="last", help="return the best match (first or last)")
    args = parser.parse_args()

    data_file = "/Users/darius90332/Algorithm-Analysis-All-Hands-Module-2/data/test_metrics.json"
    data = load_data(data_file)

    start_time = time.time()
    sorted_data = bubble_sort(data, args.attribute)
    end_time = time.time()

    best_match = sorted_data[0] if args.best == "first" else sorted_data[-1]

    print(f"Best Match: {best_match}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()