# test_generator.py

import random

SHAPES = ['Q', 'Z', 'S', 'T', 'I', 'L', 'J']

def generate_max_height_test():
    """
    Generates a test case that stacks pieces to reach the maximum allowed height.
    """
    max_height = 10**7
    # Since each piece adds at most 4 units to the height, we need max_height // 4 pieces
    num_pieces = max_height // 4
    test_pieces = []
    col = 0
    for _ in range(num_pieces):
        # Use the 'I' piece vertically to maximize height
        test_pieces.append(f"I{col}")
        col = (col + 1) % 7  # Cycle through columns to spread the pieces
    return ','.join(test_pieces)

def generate_full_row_clear_test():
    """
    Generates a test case where multiple full rows are cleared simultaneously.
    """
    test_pieces = []
    # Fill the bottom row
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
    # Second layer
    test_pieces.extend([f"S{col}" for col in range(1, 9, 2)])
    # Piece that triggers multiple row clears
    test_pieces.append("I0")
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

def generate_random_test(num_pieces, max_height):
    """
    Generates a random test case with a given number of pieces.
    """
    test_pieces = []
    for _ in range(num_pieces):
        shape = random.choice(SHAPES)
        col = random.randint(0, 9)
        test_pieces.append(f"{shape}{col}")
    return ','.join(test_pieces)

def main():
    # Test Case 1: Maximum Height Test
    with open('test_max_height.txt', 'w') as f:
        test_case = generate_max_height_test()
        f.write(test_case + '\n')

    # Test Case 2: Full Row Clear Test
    with open('test_full_row_clear.txt', 'w') as f:
        test_case = generate_full_row_clear_test()
        f.write(test_case + '\n')

    # Test Case 3: Complex Row Clear Test
    with open('test_complex_row_clear.txt', 'w') as f:
        test_case = generate_complex_row_clear_test()
        f.write(test_case + '\n')

    # Test Case 4: Out of Bounds Test
    with open('test_out_of_bounds.txt', 'w') as f:
        test_case = generate_out_of_bounds_test()
        f.write(test_case + '\n')

    # Test Case 5: Random Large Test
    with open('test_random_large.txt', 'w') as f:
        test_case = generate_random_test(num_pieces=10000, max_height=10000)
        f.write(test_case + '\n')

    print("Test cases generated.")

if __name__ == "__main__":
    main()
