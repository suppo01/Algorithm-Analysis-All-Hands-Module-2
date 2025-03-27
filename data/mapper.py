import json
import os

def map_coverage_percent_to_tests(coverage_file, test_metrics_file, output_file):
    """
    Maps coverage data from coverage.json to test_metrics.json.
    Each test gets the covered_lines/duration ratio from its corresponding module.
    
    Args:
        coverage_file: Path to coverage.json file
        test_metrics_file: Path to test_metrics.json file
        output_file: Path to save the computed test metrics
    """
    # Load the coverage and test metrics files
    with open(coverage_file, 'r') as f:
        coverage_data = json.load(f)
    
    with open(test_metrics_file, 'r') as f:
        test_metrics = json.load(f)
    
    # Create mapping from module names to their coverage data
    module_coverage = {}
    for file_path, data in coverage_data["files"].items():
        if file_path.startswith("chasten/"):
            module_name = os.path.basename(file_path).replace(".py", "")
            module_coverage[module_name] = {
                "covered_lines": data["summary"]["covered_lines"],
                "num_statements": data["summary"]["num_statements"],
                "percent_covered": data["summary"]["percent_covered"],
                "missing_lines": data["summary"]["missing_lines"],
                "excluded_lines": data["summary"]["excluded_lines"]
            }
    
    # Update each test metric with the computed covered_lines/duration ratio
    for test in test_metrics:
        test_file = test["name"].split("::")[0]
        module_name = os.path.basename(test_file).replace("test_", "").replace(".py", "")
        
        # For failed or skipped tests, set coverage to 0
        if test["outcome"] != "passed":
            test["coverage"] = 0
            continue
        
        # If we have coverage data for this module, compute covered_lines/duration
        if module_name in module_coverage:
            # Avoid division by zero by checking duration
            if test["duration"] > 0:
                test["coverage"] = test["duration"] / module_coverage[module_name]["covered_lines"] 
            else:
                test["coverage"] = 0
        else:
            # Default to 0 if no coverage data is found
            test["coverage"] = 0
    
    # Save the computed test metrics
    with open(output_file, 'w') as f:
        json.dump(test_metrics, f, indent=2)
    
    print(f"Coverage metrics successfully computed and saved to {output_file}")
    
    return test_metrics

def create_nsga_format(coverage_file, test_metrics_file, output_file):
    """
    Creates a JSON file in NSGA format with test case name, duration, and coverage.
    
    Args:
        coverage_file: Path to coverage.json file
        test_metrics_file: Path to test_metrics.json file
        output_file: Path to save the NSGA format data
    """
    # Load the coverage and test metrics files
    with open(coverage_file, 'r') as f:
        coverage_data = json.load(f)
    
    with open(test_metrics_file, 'r') as f:
        test_metrics = json.load(f)
    
    # Create mapping from module names to their coverage data
    module_coverage = {}
    for file_path, data in coverage_data["files"].items():
        if file_path.startswith("chasten/"):
            module_name = os.path.basename(file_path).replace(".py", "")
            module_coverage[module_name] = {
                "covered_lines": data["summary"]["covered_lines"]
            }
    
    # Create NSGA format data
    nsga_data = {"data": []}
    
    # Process each test metric
    for test in test_metrics:
        test_file = test["name"].split("::")[0]
        module_name = os.path.basename(test_file).replace("test_", "").replace(".py", "")
        
        # Get the coverage (lines) for this module
        coverage = 0
        if module_name in module_coverage:
            coverage = module_coverage[module_name]["covered_lines"]
        
        # Add the test data in NSGA format
        nsga_data["data"].append([
            test["name"],
            test["duration"],
            coverage
        ])
    
    # Save the NSGA format data
    with open(output_file, 'w') as f:
        json.dump(nsga_data, f, indent=2)
    
    print(f"NSGA format data successfully saved to {output_file}")
    
    return nsga_data

if __name__ == "__main__":
    map_coverage_percent_to_tests("coverage.json", "test_metrics.json", "newtryingToCompute.json")
    create_nsga_format("coverage.json", "test_metrics.json", "nsga.json")