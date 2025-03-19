import json
import os

def map_coverage_to_tests(coverage_file, test_metrics_file, output_file):
    """
    Directly maps coverage data from coverage.json to test_metrics.json without any 
    calculations. Each test gets the exact same coverage information from its 
    corresponding module in the coverage.json file.
    
    Args:
        coverage_file: Path to coverage.json file
        test_metrics_file: Path to test_metrics.json file
        output_file: Path to save the enhanced test metrics
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
                "missing_lines": data["summary"]["missing_lines"],
                "percent_covered": round(data["summary"]["percent_covered"])
            }
    
    # Update each test metric with the corresponding module's coverage data
    for test in test_metrics:
        test_file = test["name"].split("::")[0]
        module_name = os.path.basename(test_file).replace("test_", "").replace(".py", "")
        
        # For failed or skipped tests, set coverage to 0
        if test["outcome"] != "passed":
            test["coverage"] = {
                "lines": 0,
                "total_lines": 0,
                "missing_lines": 0,
                "percent_covered": 0,
                "branches": 0
            }
            continue
        
        # If we have coverage data for this module, use it directly
        if module_name in module_coverage:
            cov = module_coverage[module_name]
            test["coverage"] = {
                "lines": cov["covered_lines"],
                "total_lines": cov["num_statements"],
                "missing_lines": cov["missing_lines"],
                "percent_covered": cov["percent_covered"],
                "branches": 0  # Keep as is
            }
    
    # Save the enhanced test metrics
    with open(output_file, 'w') as f:
        json.dump(test_metrics, f, indent=2)
    
    print(f"Coverage data successfully mapped from {coverage_file} to {output_file}")
    
    # Print some validation statistics
    passed_tests = [t for t in test_metrics if t["outcome"] == "passed"]
    unique_modules = set(os.path.basename(t["name"].split("::")[0]).replace("test_", "").replace(".py", "") 
                        for t in passed_tests)
    covered_modules = set(module_coverage.keys())
    
    print(f"Number of unique test modules with passing tests: {len(unique_modules)}")
    print(f"Number of modules with coverage data: {len(covered_modules)}")
    print(f"Modules with tests but no coverage: {unique_modules - covered_modules}")
    print(f"Modules with coverage but no tests: {covered_modules - unique_modules}")
    
    return test_metrics

if __name__ == "__main__":
    map_coverage_to_tests("coverage.json", "test_metrics.json", "enhanced_test_metrics.json")