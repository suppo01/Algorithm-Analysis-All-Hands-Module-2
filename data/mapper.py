import json
import os

def map_coverage_percent_to_tests(coverage_file, test_metrics_file, output_file):
    """
    Maps only the percent_covered value from coverage.json to test_metrics.json.
    Each test gets the exact coverage percentage from its corresponding module.
    
    Args:
        coverage_file: Path to coverage.json file
        test_metrics_file: Path to test_metrics.json file
        output_file: Path to save the simplified test metrics
    """
    # Load the coverage and test metrics files
    with open(coverage_file, 'r') as f:
        coverage_data = json.load(f)
    
    with open(test_metrics_file, 'r') as f:
        test_metrics = json.load(f)
    
    # Create mapping from module names to their coverage percentage
    module_coverage_percent = {}
    for file_path, data in coverage_data["files"].items():
        if file_path.startswith("chasten/"):
            module_name = os.path.basename(file_path).replace(".py", "")
            # Round to nearest integer
            module_coverage_percent[module_name] = round(data["summary"]["percent_covered"])
    
    # Update each test metric with the corresponding module's coverage percentage
    for test in test_metrics:
        test_file = test["name"].split("::")[0]
        module_name = os.path.basename(test_file).replace("test_", "").replace(".py", "")
        
        # For failed or skipped tests, set coverage to 0
        if test["outcome"] != "passed":
            test["coverage"] = 0
            continue
        
        # If we have coverage data for this module, use it directly
        if module_name in module_coverage_percent:
            test["coverage"] = module_coverage_percent[module_name]
        else:
            # Default to 0 if no coverage data is found
            test["coverage"] = 0
    
    # Save the simplified test metrics
    with open(output_file, 'w') as f:
        json.dump(test_metrics, f, indent=2)
    
    print(f"Coverage percentages successfully mapped from {coverage_file} to {output_file}")
    
    return test_metrics

if __name__ == "__main__":
    map_coverage_percent_to_tests("coverage.json", "test_metrics.json", "simplified_test_metrics.json")