# Tetris Engine

This project implements an optimized Tetris engine that processes sequences of Tetris pieces, simulating their placement in a grid, and computes the final height of the stack after all pieces have been placed. The engine is designed with efficiency in mind, featuring improved time and space complexity over a naive implementation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Time and Space Complexity](#time-and-space-complexity)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Tetris Engine
  - [Expected Input and Output](#expected-input-and-output)
- [Testing](#testing)
  - [Generating Test Cases](#generating-test-cases)
  - [Running Tests](#running-tests)
- [Benchmark Comparison](#benchmark-comparison)
- [Error Handling](#error-handling)
- [License](#license)

## Overview

The Tetris engine reads sequences of Tetris pieces from standard input, processes them according to simplified Tetris rules, and outputs the final height of the stack after all pieces have been placed.

Key characteristics:
- Efficient handling of piece placement and row clearing.
- Optimizations to reduce time and space complexity.
- Error handling for invalid inputs and out-of-bounds placements.

**Note:** The benchmark version (`tetris_benchmark.py`) is the pre-optimized Tetris engine. It cannot handle large stress tests, such as those involving a stack height of $10^7$, due to its inefficiency.

## Features

- Supports all standard Tetris pieces:
  - Square (Q)
  - Z-shape (Z)
  - S-shape (S)
  - T-shape (T)
  - Line (I)
  - L-shape (L)
  - J-shape (J)
  <img width="378" alt="image" src="https://github.com/user-attachments/assets/f57acd09-0ec0-4051-95d6-c0edbbfc9913">

- Handles piece placement with consideration for collisions and grid boundaries.
- Efficiently checks for full rows and clears them without handling cascading clears.
- Command-line visualization option to display the grid after each piece is dropped (useful for debugging).

## Time and Space Complexity Comparison

A concise comparison of the **Pre-Optimized (Benchmark)** and **Post-Optimized** Tetris engine implementations based on the provided code.

### Time Complexity

| **Operation**           | **Pre-Optimized (Benchmark)** | **Post-Optimized**       | **Improvement**                   |
|-------------------------|-------------------------------|---------------------------|------------------------------------|
| **Placing a Piece**     | O(1)                          | O(1)                      | No change                          |
| **Collision Detection** | O(1)                          | O(1)                      | No change                          |
| **Updating Heights**    | O(H) per piece                | O(1) per piece            | From linear to constant time       |
| **Checking Full Rows**  | O(H) per piece                | O(1) per piece *(using `row_counts`)* | Eliminated linear scans            |
| **Clearing Rows**       | O(H) per cleared row          | O(1) per cleared row      | From linear to constant time       |
| **Overall Per-Piece**   | O(H)                          | O(1)                      | Significant reduction in complexity|
| **Overall Per Test Case** | O(N * H)                      | O(N)                      | From quadratic to linear           |

**Where:**
- **H** = Current height of the grid
- **N** = Number of pieces in a test case

### Space Complexity

| **Data Structure**      | **Pre-Optimized (Benchmark)** | **Post-Optimized**           | **Impact**             |
|-------------------------|-------------------------------|-------------------------------|------------------------|
| **Grid Representation** | O(H)                          | O(H)                          | No change              |
| **Column Heights**      | O(1)                          | O(1)                          | No change              |
| **Row Counts**          | Not Maintained                | O(H) *(using `row_counts`)*   | Added for efficiency  |
| **Global Offset**       | Not Used                      | O(1) *(if implemented)*       | Added for tracking     |
| **Overall Space**       | O(H)                          | O(H)                          | Maintained              |

### Summary of Improvements

- **Time Efficiency:**
  - **Pre-Optimized:** Operations like updating heights and clearing rows scale linearly with grid height **H**, leading to potential performance issues with tall stacks.
  - **Post-Optimized:** Introduced `row_counts` to track occupied blocks per row, allowing constant time **O(1)** for checking and clearing full rows.

- **Overall Per Test Case:**
  - **Pre-Optimized:** O(N * H) – Time scales quadratically with the number of pieces **N** and grid height **H**.
  - **Post-Optimized:** O(N) – Time scales linearly with the number of pieces **N**, independent of grid height.

- **Space Efficiency:**
  - **Post-Optimized** adds minimal overhead with `row_counts`, maintaining overall linear space complexity.

### Conclusion

The **Post-Optimized** Tetris engine significantly enhances performance by reducing the time complexity of critical operations from **O(H)** to **O(1)** per piece. This optimization ensures efficient handling of large grid heights and rapid row clears without increasing the space complexity. Additionally, the overall time complexity per test case improves from **O(N * H)** to **O(N)**, making the engine scalable and performant for extensive inputs.

---

## Installation

Ensure you have Python 3.6 or later installed on your system.

1. Clone the repository or download the engine files:

   ```bash
   git clone https://github.com/yayashuxue/altera-tetris.git
   ```

2. Navigate to the project directory:

   ```bash
   cd altera-tetris
   ```

## Usage

### Running the Tetris Engine

The main script is `tetris.py`, which reads input from standard input and outputs the final stack height.

**Basic Usage:**

```bash
python tetris.py < input.txt
```
**Comparing Output:**

```bash
python tetris.py < input.txt > output.txt
diff sample_output.txt output.txt
```

**With Visualization:**

To enable grid visualization after each piece is dropped, use the `--visualize` flag:

```bash
python tetris.py --visualize < input.txt
```


### Expected Input and Output

**Input Format:**
- The input consists of lines, each containing a sequence of Tetris pieces separated by commas.
- Each piece is represented by a letter followed by a column number (e.g., T0, Z3, S5).
- Column numbers range from 0 to 9, representing the leftmost column where the piece is placed.

Example Input (checkout input.txt for full example):
```
Q1,Q4,Q7,L0,T2,T5,J8
```

**Output Format:**
- The output is a single integer representing the final height of the stack after all pieces have been placed.
- If an error occurs (e.g., a piece goes out of bounds or a collision is detected), the engine outputs -1.

Example Output () :
```
4
```

**Out-of-Bounds Handling:**
- If a piece is placed outside the grid horizontally (column less than 0 or greater than 9), or if a collision occurs, the engine outputs -1.

## Testing

### Generating Test Cases

The `test_generator.py` script can generate various test cases under `tests/` directory to evaluate the engine's performance and correctness.

**Generating Tests:**

```bash
python test_generator.py
```

This will create multiple test files in the `tests/` directory, such as:
- `test_max_height.txt`
- `test_full_row_clear.txt`
- `test_complex_row_clear.txt`
- `test_out_of_bounds.txt`
- `test_random_large.txt`
- `test_max_width.txt`
- `test_stress.txt`
- `test_alternating_clear.txt`
- `test_invalid_input.txt`

### Running Tests

Go to `tests/` directory. The `run_tests.py` script executes the test cases and logs the results.

**Running All Tests:**

```bash
python run_tests.py
```

**Running a Specific Test:**

```bash
python run_tests.py --test test_max_height
```

**Running Tests with Benchmark Comparison:**

To compare the optimized engine against the benchmark version, use the `--benchmark` flag:

```bash
python run_tests.py --benchmark
```

**Enforcing a Timeout:**

Each test case has a hard cutoff of 30 seconds. If a test exceeds this time limit, it will be terminated, and the log will indicate a timeout.

## Benchmark Comparison

The benchmark version (`tetris_benchmark.py`) is the pre-optimized Tetris engine. It is included for comparison purposes and cannot handle large stress tests due to inefficiency.

Below is a table summarizing the test results when running against the benchmark:

| Test Name | Optimized Version | Benchmark Version | Outputs Match |
|-----------|-------------------|-------------------|---------------|
| test_max_height | Time: 15.3812 sec<br>Memory: 985694208 KB<br>Errors: None | Status: Timed out after 30 seconds.<br>Errors: None | No |
| test_random_large | Time: 0.1033 sec<br>Memory: 985694208 KB<br>Errors: None | Time: 0.0665 sec<br>Memory: 985694208 KB<br>Errors: None | Yes |
| test_sample_input | Time: 0.0887 sec<br>Memory: 985694208 KB<br>Errors: None | Time: 0.0691 sec<br>Memory: 985694208 KB<br>Errors: None | Yes |
| test_complex_row_clear | Time: 0.0907 sec<br>Memory: 985694208 KB<br>Errors: None | Time: 0.0696 sec<br>Memory: 985694208 KB<br>Errors: None | Yes |
| test_out_of_bounds | Time: 0.0862 sec<br>Memory: 985694208 KB<br>Errors: None | Time: 0.0705 sec<br>Memory: 985694208 KB<br>Errors: None | Yes |
| test_full_row_clear | Time: 0.0860 sec<br>Memory: 985694208 KB<br>Errors: None | Time: 0.0666 sec<br>Memory: 985694208 KB<br>Errors: None | Yes |

**Notes:**
- The benchmark version timed out on `test_max_height` due to its inability to handle large stack heights efficiently.
- The optimized version successfully completed `test_max_height` within the time limit.
- For other tests, both versions produced matching outputs.
- Memory usage values are placeholders and may vary based on system specifications.

**Interpreting the Results:**
- **Time Efficiency:** The optimized version demonstrates improved performance on large inputs where the benchmark fails or is slower.
- **Correctness:** Outputs match between the optimized and benchmark versions for tests where the benchmark can complete, indicating that optimizations did not compromise functionality.

**Viewing Test Results:**

Test results are logged in `tests/test_results.log`. The log includes execution time, memory usage, errors, and output comparison results.

## Error Handling

The engine handles errors gracefully:

**Out-of-Bounds Placement:**
- If a piece is placed outside the grid horizontally (column less than 0 or greater than 9), or if a collision occurs, the engine outputs -1.

**Collision Detection:**
- If a collision is detected when placing a piece (i.e., it overlaps with existing blocks), the engine outputs -1.

**Invalid Inputs:**
- If an invalid piece identifier is provided, the engine skips that piece and continues processing the remaining pieces.
- For invalid column numbers, the engine outputs -1 as per out-of-bounds handling.

Example of Error Output:
```
-1
```

## AI Tools and Prompt Use
This app uses `gpt-o1-preview` and `claude 3.5 sonnet`, and only the prior one is mainly effective.
To write effective prompt to `gpt-o1-preview`, **directly instruct them to understand the rules (especially edge case & boundaries) & goals while restricting them to go straight to write code**. Ask them to clearly align their understanding of the problem & the world with the user is important to solve complex problem. For example, the LLM always messed up about generating the right orientation of the `SHAPES` of tetris, till I explicitly ask them to align (0,0) as the bottom left of the tetris game world. Also, I get stuck for a long while till I realize the tetris game has 'cascading row clearing' (which is actually not needed for this engine), which increases the time complexity a lot.

**Prompt use**

(Pre-optimized benchmark file): help me solve this tetris problem. instructions as below. before you dive deep into the code base, write down your understanding of the problem, and the boundary of the problem, in a straight forward and concise way. you need to understand the boundary very well to solve it, any hallucination or assumption of the problem would ruin it. shape: (i ask gpt-4o to write it first and  check the SHAPES part and give the code of its coordinates to them) ... PASTED FROM DOCUMENT

## License

This project is licensed under the MIT License.
