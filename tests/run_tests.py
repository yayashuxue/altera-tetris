import argparse
import os
import subprocess
import sys
import time
import resource

# Define paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to the 'tests/' directory
ENGINE_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))  # Parent directory containing 'tetris.py'

OUTPUT_DIR = os.path.join(TEST_DIR, 'outputs')
LOG_FILE = os.path.join(TEST_DIR, 'test_results.log')

# Ensure the outputs directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

test_files = []

parser = argparse.ArgumentParser(description="Run Tetris engine tests.")
parser.add_argument('--test', type=str, help="Specify a single test to run (without extension).")
parser.add_argument('--benchmark', action='store_true', help="Run tests against the benchmark version.")
args = parser.parse_args()

# Get test files
if args.test:
    test_files = [f"{args.test}.txt"]
else:
    test_files = [f for f in os.listdir(TEST_DIR) if f.endswith('.txt')]

# Initialize the log file
with open(LOG_FILE, 'w') as log:
    log.write("Test Results:\n")
    log.write("=============\n\n")

for test_file in test_files:
    test_name = os.path.splitext(test_file)[0]
    test_path = os.path.join(TEST_DIR, test_file)
    output_file_optimized = os.path.join(OUTPUT_DIR, f"{test_name}_optimized_output.txt")
    output_file_benchmark = os.path.join(OUTPUT_DIR, f"{test_name}_benchmark_output.txt") if args.benchmark else None

    print(f"Running test: {test_name}")

    # Paths to the scripts
    TETRIS_OPTIMIZED_SCRIPT = os.path.join(ENGINE_DIR, 'tetris.py')
    TETRIS_BENCHMARK_SCRIPT = os.path.join(ENGINE_DIR, 'tetris_benchmark.py') if args.benchmark else None

    # Dictionaries to hold metrics
    metrics = {
        'optimized': {'time': None, 'memory': None, 'errors': None, 'timed_out': False},
    }

    if args.benchmark:
        metrics['benchmark'] = {'time': None, 'memory': None, 'errors': None, 'timed_out': False}

    # Define versions to test
    versions = [('optimized', TETRIS_OPTIMIZED_SCRIPT, output_file_optimized)]
    if args.benchmark:
        versions.append(('benchmark', TETRIS_BENCHMARK_SCRIPT, output_file_benchmark))

    for version, script_path, output_file in versions:
        # Command to run the tetris script
        cmd = [sys.executable, script_path]

        # Start time
        start_time = time.time()

        # Open input and output files
        with open(test_path, 'r') as infile, open(output_file, 'w') as outfile:
            # Run the tetris script
            proc = subprocess.Popen(
                cmd,
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # To ensure resource limits are enforced
            )

            try:
                # Wait for the process to complete with a timeout
                _, stderr = proc.communicate(timeout=30)
                end_time = time.time()
                elapsed_time = end_time - start_time
                metrics[version]['time'] = elapsed_time
                metrics[version]['memory'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                metrics[version]['errors'] = stderr.decode('utf-8') if stderr else None
            except subprocess.TimeoutExpired:
                # If the process takes longer than 30 seconds, kill it
                proc.kill()
                _, stderr = proc.communicate()
                end_time = time.time()
                elapsed_time = end_time - start_time
                metrics[version]['time'] = elapsed_time
                metrics[version]['memory'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                metrics[version]['errors'] = 'Test timed out after 30 seconds.'
                metrics[version]['timed_out'] = True

        # If the test timed out, ensure the output file is empty
        if metrics[version]['timed_out']:
            with open(output_file, 'w') as outfile:
                outfile.write('')

    # Compare outputs only if benchmark is run and neither version timed out
    if args.benchmark and not metrics['benchmark']['timed_out'] and not metrics['optimized']['timed_out']:
        with open(output_file_benchmark, 'r') as f1, open(output_file_optimized, 'r') as f2:
            output_benchmark = f1.read()
            output_optimized = f2.read()
            outputs_match = output_benchmark == output_optimized
    else:
        outputs_match = None  # Not applicable

    # Log the results
    with open(LOG_FILE, 'a') as log:
        log.write(f"Test: {test_name}\n")
        for version in ['optimized', 'benchmark'] if args.benchmark else ['optimized']:
            log.write(f"  {version.capitalize()} Version:\n")
            if metrics[version]['timed_out']:
                log.write("    Status: Timed out after 30 seconds.\n")
            else:
                log.write(f"    Time: {metrics[version]['time']:.4f} seconds\n")
                log.write(f"    Memory: {metrics[version]['memory']} KB\n")
                if metrics[version]['errors']:
                    log.write(f"    Errors:\n{metrics[version]['errors']}\n")
                else:
                    log.write("    Errors: None\n")
        if args.benchmark:
            log.write(f"  Outputs Match: {'Yes' if outputs_match else 'No'}\n")
        log.write("\n")

    print(f"Test {test_name} completed. Results logged.")

print(f"All tests completed. Results are logged in {LOG_FILE}.")
