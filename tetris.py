import sys

# Define the shapes as lists of (row, column) positions
SHAPES = {
    'Q': [(0, 0), (0, 1), (1, 0), (1, 1)],      # Square
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)],      # Z-shape
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],      # S-shape
    'T': [(0, 0), (0, 1), (0, 2), (1, 1)],      # T-shape
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],      # Line 
    'L': [(0, 0), (1, 0), (2, 0), (2, 1)],      # L-shape
    'J': [(0, 1), (1, 1), (2, 0), (2, 1)]       # J-shape
}
# Characters for each shape
SHAPES_CHARS_DISPLAY = {
    'Q': 'Q',
    'Z': 'Z',
    'S': 'S',
    'T': 'T',
    'I': 'I',
    'L': 'L',
    'J': 'J'
}

# Function to print shapes with characters as specified by the user
def print_shape_with_chars(shape_coords, char):
    # Find the max dimensions to create the grid
    max_x = max([x for x, y in shape_coords])
    max_y = max([y for x, y in shape_coords])
    
    # Create a grid of '.' to represent empty spaces
    grid = [['.' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    
    # Place the specified character in the grid where the shape's coordinates are
    for x, y in shape_coords:
        grid[x][y] = char
    
    # Print the grid
    for row in grid:
        print(" ".join(row))

# # Print all corrected shapes with their respective characters
# # Helper function to print the shapes
# for shape, coords in SHAPES.items():
#     print(f"Shape: {shape}")
#     print_shape_with_chars(coords, SHAPES_CHARS_DISPLAY[shape])
#     print("\n")  # Add some space between shapes



# tetris.py

def drop_piece(grid, shape_positions, left_col):
    # Adjust the shape positions with the left_col
    adjusted_positions = [(row_offset, col_offset + left_col) for (row_offset, col_offset) in shape_positions]
    # Verify that all columns are within 0 to 9
    for row_offset, col in adjusted_positions:
        if col < 0 or col >= 10:
            raise ValueError("Piece goes outside the grid horizontally")

    # Initialize vertical_offset
    if grid:
        max_row = max(grid.keys())
    else:
        max_row = -1
    vertical_offset = max_row + 5  # Start above the current highest block

    while True:
        collision = False
        positions = []
        for row_offset, col in adjusted_positions:
            row = vertical_offset - row_offset
            if row < 0 or col < 0 or col >=10 or (row in grid and col in grid[row]):
                collision = True
                break
            positions.append((row, col))
        if collision:
            vertical_offset += 1  # Place the piece at the previous vertical_offset
            break
        else:
            vertical_offset -= 1  # Move the piece down by 1

    # Place the piece at vertical_offset
    final_positions = []
    for row_offset, col in adjusted_positions:
        row = vertical_offset - row_offset
        if row not in grid:
            grid[row] = set()
        grid[row].add(col)
        final_positions.append((row, col))

    return final_positions

def adjust_grid(grid, cleared_rows):
    # Build a mapping from old_row to new_row
    cleared_rows_set = set(cleared_rows)
    row_mapping = {}
    num_cleared = 0
    new_grid = {}
    for row in sorted(grid.keys()):
        if row in cleared_rows_set:
            num_cleared += 1
        else:
            new_row = row - num_cleared
            row_mapping[row] = new_row
            new_grid[new_row] = grid[row]

    return new_grid

def process_line(line):
    grid = {}  # row number -> set of occupied columns
    pieces = line.strip().split(',')

    for piece_entry in pieces:
        if not piece_entry:
            continue
        shape_letter = piece_entry[0]
        left_col = int(piece_entry[1])
        shape_positions = SHAPES[shape_letter]

        # Drop the piece into the grid
        try:
            final_positions = drop_piece(grid, shape_positions, left_col)
        except ValueError:
            # Piece goes outside the grid; skip or handle as needed
            continue

        # Check for full rows
        rows_to_check = set([row for (row, _) in final_positions])
        cleared_rows = []
        for row in rows_to_check:
            if len(grid[row]) == 10:
                cleared_rows.append(row)

        # Adjust the grid after clearing rows
        if cleared_rows:
            grid = adjust_grid(grid, sorted(cleared_rows))

    # Determine the final height
    if not grid:
        height = 0
    else:
        height = max(grid.keys()) + 1
    print(height)

def main():
    lines = sys.stdin.read().splitlines()
    for line in lines:
        process_line(line)

if __name__ == "__main__":
    main()
