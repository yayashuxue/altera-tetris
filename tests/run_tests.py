# run_tests.py

import argparse
import os
import subprocess
import sys
import time
import resource

# Define paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TETRIS_SCRIPT = os.path.join(TEST_DIR, '..', 'tetris.py')
OUTPUT_DIR = os.path.join(TEST_DIR, 'outputs')
LOG_FILE = os.path.join(TEST_DIR, 'test_results.log')

# Ensure the outputs directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize the log file
with open(LOG_FILE, 'w') as log:
    log.write("Test Results:\n")
    log.write("=============\n\n")

test_files = []

parser = argparse.ArgumentParser(description="Run Tetris engine tests.")
parser.add_argument('--test', type=str, help="Specify a single test to run (without extension).")
args = parser.parse_args()

# Get test files
if args.test:
    test_files = [f"{args.test}.txt"]
else:
    test_files = [f for f in os.listdir(TEST_DIR) if f.endswith('.txt')]



for test_file in test_files:
    test_name = os.path.splitext(test_file)[0]
    test_path = os.path.join(TEST_DIR, test_file)
    output_file = os.path.join(OUTPUT_DIR, f"{test_name}_output.txt")
    metrics_file = os.path.join(OUTPUT_DIR, f"{test_name}_metrics.txt")

    print(f"Running test: {test_name}")

    # Command to run the tetris.py script
    cmd = [sys.executable, TETRIS_SCRIPT]

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

        # Wait for the process to complete and get resource usage
        _, stderr = proc.communicate()
        end_time = time.time()
        elapsed_time = end_time - start_time
        max_memory = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss

    # Log the results
    with open(LOG_FILE, 'a') as log:
        log.write(f"Test: {test_name}\n")
        log.write(f"\tTime: {elapsed_time:.2f} seconds\n")
        log.write(f"\tMemory: {max_memory} KB\n")
        if stderr:
            log.write(f"\tErrors:\n{stderr.decode('utf-8')}\n")
        log.write("\n")

print(f"All tests completed. Results are logged in {LOG_FILE}.")
