import functools
import sys
import time
from typing import List
import argparse

def bubble_sort(numbers: List[int]) -> List[int]:
    """Sort a list of numbers using the bubble sort algorithm."""
    n = len(numbers)  # grabs the number of elements in the list
    for i in range(n):  # loop through all elements in the list
        for j in range(0, n - i - 1):  # loop through all elements in the list from 0 to n-i-1
            # Switch if the element found is greater than the next element
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers

def main():
    parser = argparse.ArgumentParser(description="Sort a list of numbers using bubble sort.")
    parser.add_argument("numbers", metavar="N", type=int, nargs="+", help="an integer for the list to sort")
    args = parser.parse_args()

    numbers = args.numbers
    start_time = time.time()
    sorted_numbers = bubble_sort(numbers)
    end_time = time.time()

    print(f"Sorted numbers: {sorted_numbers}")
    print(f"Time taken: {end_time - start_time:.6f}")

if __name__ == "__main__":
   main()