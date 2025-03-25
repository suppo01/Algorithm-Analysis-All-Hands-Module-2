from quick_sort import measure_sorting_time
from tabulate import tabulate  # Import the tabulate library

# Path to your test metrics file
# file_path = '../data/test_metrics.json'  # Update the path to include the parent folder
file_path = '../data/simplified_test_metrics.json'  # Updated path to the correct file


# mesure running time this is where it gets called
# Sort by duration (you can change to 'coverage' or any other key that is prefer)

sorted_tests = measure_sorting_time(file_path, 'duration')
sorted_tests = measure_sorting_time(file_path, 'coverage')


# Prepare data for tabular display
table_data = [[test['name'], test['duration'], test['coverage']] for test in sorted_tests]
headers = ["Test Name", "Duration", "Coverage"]

# Print the table
print(tabulate(table_data, headers=headers, tablefmt="grid"))
