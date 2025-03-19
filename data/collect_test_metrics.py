"""Script to collect test execution metrics for NSGA-II comparison research."""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
import subprocess

def run_tests_with_coverage() -> Dict[str, Any]:
    """Run tests with coverage and JSON report enabled."""
    start_time = time.time()
    
    # Run tests using poetry run task test
    cmd = [
        "poetry", "run", "task", "test",
        "--cov",
        "--cov-report=json:coverage.json",
        "--json-report",
        "--json-report-file=test_report.json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running tests: {result.stderr}")
            return {}
            
        end_time = time.time()
        
        # Read the coverage JSON file
        try:
            with open("coverage.json", "r") as f:
                coverage_data = json.load(f)
        except FileNotFoundError:
            print("Warning: coverage.json not found.")
            coverage_data = {}
            
        # Read the test report JSON file
        try:
            with open("test_report.json", "r") as f:
                test_report = json.load(f)
        except FileNotFoundError:
            print("Warning: test_report.json not found.")
            test_report = {"tests": []}
        
        return {
            "total_time": end_time - start_time,
            "test_results": test_report,
            "coverage_data": coverage_data
        }
        
    except Exception as e:
        print(f"Error executing tests: {e}")
        return {}

def normalize_path(path: str) -> str:
    """Normalize a file path for comparison."""
    return str(Path(path).resolve())

def extract_test_metrics(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract relevant metrics from test results."""
    metrics = []
    
    # Get test results from the report
    for test in data["test_results"].get("tests", []):
        # Extract test name and duration from the report
        test_name = test.get("nodeid", "unknown")
        test_duration = test.get("duration", 0.0)  # Get duration directly from test result
        test_outcome = test.get("outcome", "unknown")
        
        # Create test metrics with initial coverage values
        test_metrics = {
            "name": test_name,
            "duration": test_duration,
            "outcome": test_outcome,
            "coverage": {
                "lines": 0,
                "branches": 0,
                "missing_lines": 0
            }
        }
        
        # Update coverage information from coverage data
        coverage_data = data["coverage_data"]
        if isinstance(coverage_data, dict):
            # Extract the test file path from the test name
            test_file = test_name.split("::")[0]
            test_file_normalized = normalize_path(test_file)
            
            # Look for coverage data in the corresponding file
            for file_path, file_data in coverage_data.get("files", {}).items():
                file_path_normalized = normalize_path(file_path)
                if test_file_normalized in file_path_normalized:
                    # Get total lines and branches in the file
                    total_lines = file_data.get("summary", {}).get("num_statements", 0)
                    total_branches = file_data.get("summary", {}).get("num_branches", 0)
                    
                    # Count lines and branches covered by this test
                    covered_lines = 0
                    covered_branches = 0
                    missing_lines = 0
                    
                    # Process each line in the file
                    for line_num, line_data in file_data.get("lines", {}).items():
                        # Check if this test covers this line
                        if test_name in line_data.get("tests", []):
                            covered_lines += 1
                            # Check branch coverage
                            if line_data.get("branches"):
                                for branch in line_data["branches"]:
                                    if test_name in branch.get("tests", []):
                                        covered_branches += 1
                        # Count missing lines
                        elif line_data.get("missing"):
                            missing_lines += 1
                    
                    # Update test metrics with coverage information
                    test_metrics["coverage"].update({
                        "lines": covered_lines,
                        "branches": covered_branches,
                        "missing_lines": missing_lines,
                        "total_lines": total_lines,
                        "total_branches": total_branches,
                        "line_coverage_percentage": (covered_lines / total_lines * 100) if total_lines > 0 else 0,
                        "branch_coverage_percentage": (covered_branches / total_branches * 100) if total_branches > 0 else 0
                    })
                    
                    # Print debug information
                    print(f"Found coverage for test {test_name}:")
                    print(f"  File: {file_path}")
                    print(f"  Covered lines: {covered_lines}/{total_lines}")
                    print(f"  Covered branches: {covered_branches}/{total_branches}")
        
        metrics.append(test_metrics)
    
    return metrics

def save_metrics(metrics: List[Dict[str, Any]], output_file: str):
    """Save collected metrics to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)

def main():
    """Main function to collect and save test metrics."""
    # Create output directory if it doesn't exist
    output_dir = Path("test_metrics")
    output_dir.mkdir(exist_ok=True)
    
    # Collect metrics
    data = run_tests_with_coverage()
    metrics = extract_test_metrics(data)
    
    # Save metrics
    output_file = output_dir / "test_metrics.json"
    save_metrics(metrics, str(output_file))
    print(f"Metrics saved to {output_file}")

if __name__ == "__main__":
    main() 