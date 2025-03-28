from quick_sort import measure_sorting_time
from tabulate import tabulate  # Import the tabulate library

# Path to your test metrics file
# file_path = '../data/simplified_test_metrics.json'  # Updated path to the correct file
file_path = '../data/tryingToCompute.json'  # Updated to new file

# Function to find the fastest test case
def find_fastest_test_case(sorted_tests):
    # Start with the first test case as the fastest
    fastest_test = sorted_tests[0]

    # Loop through all test cases to find the one with the smallest duration
    for test in sorted_tests:
        if test['duration'] < fastest_test['duration']:
            fastest_test = test  # Update the fastest test case

    return fastest_test  # Return the test case with the smallest duration

# Measure running time and sort by duration
sorted_tests_by_duration = measure_sorting_time(file_path, 'duration')
# Sort by coverage (if you want this, otherwise leave out)
sorted_tests_by_coverage = measure_sorting_time(file_path, 'coverage')

# Find the fastest test case (best outcome)
fastest_test_case = find_fastest_test_case(sorted_tests_by_duration)

# Print the fastest test case
print("Fastest Test Case (Base on duration):")
print(f"Test Name: {fastest_test_case['name']}")
print(f"Duration: {fastest_test_case['duration']}")
print(f"Coverage: {fastest_test_case['coverage']}")


# Prepare data for tabular display (for sorted by coverage)
# table_data = [[test['name'], test['duration'], test['coverage']] for test in sorted_tests_by_duration]
table_data = [[test['name'], test['duration'], test['coverage']] for test in sorted_tests_by_coverage[:10]]
headers = ["Test Name", "Duration", "Coverage"]

# Print the table of sorted test cases
# print("\nSorted Test Cases by Duration:")
print("\nSorted Test Cases by Coverage:")
print(tabulate(table_data, headers=headers, tablefmt="grid"))

