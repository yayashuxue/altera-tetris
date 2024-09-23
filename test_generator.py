import random

SHAPES = ['Q', 'Z', 'S', 'T', 'I', 'L', 'J']

def generate_max_height_test():
    """
    Generates a test case that stacks pieces to reach the maximum allowed height.
    """
    max_height = 1000  # Adjusted to a reasonable value for testing
    num_pieces = max_height // 4
    test_pieces = []
    col = 0
    for _ in range(num_pieces):
        # Use the 'I' piece vertically to maximize height
        test_pieces.append(f"I{col}")
        col = (col + 1) % 10  # Cycle through columns to spread the pieces
    return ','.join(test_pieces)

def generate_full_row_clear_test():
    """
    Generates a test case where multiple full rows are cleared simultaneously.
    """
    test_pieces = []
    # Fill the bottom two rows completely
    for row in range(2):
        for col in range(0, 10, 2):
            test_pieces.append(f"Q{col}")
    # Add a piece that completes the next row and triggers a clear
    test_pieces.append("I0")
    return ','.join(test_pieces)

def generate_complex_row_clear_test():
    """
    Generates a test case with interleaved row fills and clears.
    """
    test_pieces = []
    # First layer
    test_pieces.extend([f"Q{col}" for col in range(0, 10, 2)])
    # Second layer with gaps
    test_pieces.extend([f"S{col}" for col in range(1, 9, 2)])
    # Pieces to fill gaps and trigger multiple row clears
    test_pieces.append("Z1")
    test_pieces.append("T3")
    test_pieces.append("L5")
    test_pieces.append("J7")
    return ','.join(test_pieces)

def generate_out_of_bounds_test():
    """
    Generates a test case where pieces are placed outside the grid bounds.
    """
    test_pieces = []
    test_pieces.append("Q-1")   # Invalid negative column
    test_pieces.append("I10")   # Invalid column beyond grid width
    test_pieces.append("T9")    # Valid placement at the edge
    return ','.join(test_pieces)

def generate_random_test(num_pieces):
    """
    Generates a random test case with a given number of pieces.
    """
    test_pieces = []
    for _ in range(num_pieces):
        shape = random.choice(SHAPES)
        col = random.randint(0, 9)
        test_pieces.append(f"{shape}{col}")
    return ','.join(test_pieces)

def generate_max_width_test():
    """
    Generates a test case that fills the grid horizontally.
    """
    test_pieces = []
    for row in range(5):
        for col in range(0, 10, 4):
            test_pieces.append(f"I{col}")
    return ','.join(test_pieces)

def generate_stress_test():
    """
    Generates a stress test with a large number of random pieces.
    """
    num_pieces = 50000  # Adjust based on system capability
    return generate_random_test(num_pieces)

def generate_alternating_clear_test():
    """
    Generates a test case with alternating row fills and clears.
    """
    test_pieces = []
    # Fill even rows
    for row in range(0, 10, 2):
        for col in range(0, 10, 2):
            test_pieces.append(f"Q{col}")
    # Add pieces to fill odd rows and trigger clears
    for row in range(1, 10, 2):
        for col in range(1, 10, 2):
            test_pieces.append(f"Q{col}")
    return ','.join(test_pieces)

def generate_invalid_input_test():
    """
    Generates a test case with invalid piece identifiers and columns.
    """
    test_pieces = []
    test_pieces.append("X5")    # Invalid shape
    test_pieces.append("Q-2")   # Invalid negative column
    test_pieces.append("I11")   # Column beyond grid width
    test_pieces.append("S5")
    return ','.join(test_pieces)

def main():
    # Test Case 1: Maximum Height Test
    with open('tests/test_max_height.txt', 'w') as f:
        test_case = generate_max_height_test()
        f.write(test_case + '\n')

    # Test Case 2: Full Row Clear Test
    with open('tests/test_full_row_clear.txt', 'w') as f:
        test_case = generate_full_row_clear_test()
        f.write(test_case + '\n')

    # Test Case 3: Complex Row Clear Test
    with open('tests/test_complex_row_clear.txt', 'w') as f:
        test_case = generate_complex_row_clear_test()
        f.write(test_case + '\n')

    # Test Case 4: Out of Bounds Test
    with open('tests/test_out_of_bounds.txt', 'w') as f:
        test_case = generate_out_of_bounds_test()
        f.write(test_case + '\n')

    # Test Case 5: Random Large Test
    with open('tests/test_random_large.txt', 'w') as f:
        test_case = generate_random_test(num_pieces=10000)
        f.write(test_case + '\n')

    # Test Case 6: Maximum Width Test
    with open('tests/test_max_width.txt', 'w') as f:
        test_case = generate_max_width_test()
        f.write(test_case + '\n')

    # Test Case 7: Stress Test
    with open('tests/test_stress.txt', 'w') as f:
        test_case = generate_stress_test()
        f.write(test_case + '\n')

    # Test Case 8: Alternating Clear Test
    with open('tests/test_alternating_clear.txt', 'w') as f:
        test_case = generate_alternating_clear_test()
        f.write(test_case + '\n')

    # Test Case 9: Invalid Input Test
    with open('tests/test_invalid_input.txt', 'w') as f:
        test_case = generate_invalid_input_test()
        f.write(test_case + '\n')

    print("Test cases generated.")

if __name__ == "__main__":
    main()