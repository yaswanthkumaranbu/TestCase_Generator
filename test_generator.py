import time
import json
import statistics
from datetime import datetime
import concurrent.futures

# Performance Testing
class PerformanceTest:
    def __init__(self):
        self.response_times = []
        self.error_count = 0
        self.total_requests = 0

    def measure_response_time(self, func, *args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        response_time = end_time - start_time
        self.response_times.append(response_time)
        return result

    def calculate_statistics(self):
        if not self.response_times:
            return {
                'mean_response_time': 0,
                'median_response_time': 0,
                'max_response_time': 0,
                'min_response_time': 0,
                'total_requests': 0,
                'error_rate': 0
            }
        
        return {
            'mean_response_time': statistics.mean(self.response_times),
            'median_response_time': statistics.median(self.response_times),
            'max_response_time': max(self.response_times),
            'min_response_time': min(self.response_times),
            'total_requests': self.total_requests,
            'error_rate': self.error_count / self.total_requests if self.total_requests > 0 else 0
        }

# Accuracy Testing
class AccuracyTest:
    def __init__(self):
        self.expected_fields = ['TC_ID', 'TC_Summary', 'Description', 'Test Steps', 
                              'Expected Result', 'Actual Result', 'Status']
        self.validation_results = []

    def validate_test_case_structure(self, test_case):
        # Check if all required fields are present
        return all(field in test_case for field in self.expected_fields)

    def validate_test_case_content(self, test_case):
        errors = []
        
        # Validate TC_ID format
        if not test_case['TC_ID'].startswith('TC_'):
            errors.append(f"Invalid TC_ID format: {test_case['TC_ID']}")
        
        # Validate Test Steps
        if not isinstance(test_case['Test Steps'], list):
            errors.append("Test Steps must be a list")
        
        # Validate Expected Result
        if not isinstance(test_case['Expected Result'], list):
            errors.append("Expected Result must be a list")
        
        return errors

# Test Suite
class TestCaseGeneratorTest:
    def __init__(self):
        self.performance_test = PerformanceTest()
        self.accuracy_test = AccuracyTest()

    def run_performance_test(self, num_requests=5):
        """Run performance tests with multiple requests"""
        print(f"\nRunning performance test with {num_requests} requests...")
        
        for i in range(num_requests):
            try:
                self.performance_test.total_requests += 1
                result = self.performance_test.measure_response_time(
                    generate_test_cases, 
                    query
                )
                print(f"Request {i+1}: Completed")
            except Exception as e:
                self.performance_test.error_count += 1
                print(f"Request {i+1}: Failed - {str(e)}")

        stats = self.performance_test.calculate_statistics()
        print("\nPerformance Test Results:")
        print(f"Mean Response Time: {stats['mean_response_time']:.2f} seconds")
        print(f"Median Response Time: {stats['median_response_time']:.2f} seconds")
        print(f"Max Response Time: {stats['max_response_time']:.2f} seconds")
        print(f"Min Response Time: {stats['min_response_time']:.2f} seconds")
        print(f"Error Rate: {stats['error_rate']*100:.2f}%")

    def run_accuracy_test(self, num_test_cases=3):
        """Run accuracy tests on generated test cases"""
        print(f"\nRunning accuracy test with {num_test_cases} test cases...")
        
        for i in range(num_test_cases):
            try:
                result = generate_test_cases(query)
                test_cases = json.loads(result)
                
                if isinstance(test_cases, list):
                    for test_case in test_cases:
                        # Validate structure
                        if not self.accuracy_test.validate_test_case_structure(test_case):
                            print(f"Test Case {i+1}: Missing required fields")
                            continue
                        
                        # Validate content
                        errors = self.accuracy_test.validate_test_case_content(test_case)
                        if errors:
                            print(f"Test Case {i+1}: Content validation errors - {errors}")
                        else:
                            print(f"Test Case {i+1}: Valid")
                else:
                    print(f"Test Case {i+1}: Invalid format - expected list")
                    
            except Exception as e:
                print(f"Test Case {i+1}: Failed - {str(e)}")

    def run_concurrent_test(self, num_requests=3):
        """Run concurrent performance test"""
        print(f"\nRunning concurrent test with {num_requests} requests...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(generate_test_cases, query) for _ in range(num_requests)]
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    result = future.result()
                    print(f"Concurrent Request {i+1}: Completed")
                except Exception as e:
                    print(f"Concurrent Request {i+1}: Failed - {str(e)}")

# Run tests
if __name__ == '__main__':
    # Import the generate_test_cases function and query from main.py
    from main import generate_test_cases, query
    
    test_suite = TestCaseGeneratorTest()
    
    # Run performance test
    test_suite.run_performance_test(num_requests=3)
    
    # Run accuracy test
    test_suite.run_accuracy_test(num_test_cases=2)
    
    # Run concurrent test
    # test_suite.run_concurrent_test(num_requests=2)