import sys

# Define the shapes as lists of (row, column) positions
SHAPES = {
    'Q': [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
    'Z': [(1, 0), (1, 1), (0, 1), (0, 2)],  # Z-shape
    'S': [(1, 1), (1, 2), (0, 0), (0, 1)],  # S-shape
    'T': [(1, 0), (1, 1), (1, 2), (0, 1)],  # T-shape
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],  # Line (horizontal)
    'L': [(0, 0), (1, 0), (2, 0), (0, 1)],  # L-shape
    'J': [(0, 1), (1, 1), (2, 1), (0, 0)]   # J-shape
}
def print_shape(shape_letter):
    shape_positions = SHAPES.get(shape_letter)
    if not shape_positions:
        print(f"Shape '{shape_letter}' is not defined.")
        return
    # Find the dimensions of the shape
    max_row = max(pos[0] for pos in shape_positions)
    max_col = max(pos[1] for pos in shape_positions)
    # Create a grid for the shape
    grid = [['.' for _ in range(max_col + 1)] for _ in range(max_row + 1)]
    for row_offset, col_offset in shape_positions:
        grid[row_offset][col_offset] = shape_letter
    # Print the grid
    print(f"Shape '{shape_letter}':")
    for row in reversed(grid):  # reverse to print from top to bottom
        print(''.join(row))
    print()

import argparse


def drop_piece(grid, column_heights, shape_letter, shape_positions, left_col, visualize=False):
    # Adjust the shape positions with the left_col
    adjusted_positions = [(row_offset, col_offset + left_col) for (row_offset, col_offset) in shape_positions]
    # Verify that all columns are within 0 to 9
    for row_offset, col in adjusted_positions:
        if col < 0 or col >= 10:
            raise ValueError("Piece goes outside the grid horizontally")
    # Determine the landing row based on column heights
    # For each block, landing_row >= column_heights[col] - row_offset
    landing_row_candidates = [column_heights[col] - row_offset for row_offset, col in adjusted_positions]
    landing_row = max(landing_row_candidates)
    if landing_row < 0:
        landing_row = 0  # Ensure the piece does not go above the top of the grid
    # Check for collision at the landing position
    for row_offset, col in adjusted_positions:
        row = landing_row + row_offset
        if row in grid and col in grid[row]:
            raise ValueError("Collision detected when placing the piece")
    # Place the piece at landing_row + row_offset
    for row_offset, col in adjusted_positions:
        row = landing_row + row_offset
        if row not in grid:
            grid[row] = {}
        grid[row][col] = shape_letter  # Store the shape letter in the cell
    # Update column heights
    for col in range(10):
        # Find the highest occupied cell in the column
        occupied_rows = [row for row in grid if col in grid[row]]
        if occupied_rows:
            column_heights[col] = max(occupied_rows) + 1
        else:
            column_heights[col] = 0
    if visualize:
        print("After dropping piece:")
        print_grid(grid)
    # Check for full rows and handle cascading clears
    while True:
        full_rows = [row for row in grid if len(grid[row]) == 10]
        if not full_rows:
            break
        # Remove full rows and adjust the grid and column heights
        adjust_grid(grid, column_heights, sorted(full_rows))
        if visualize:
            print(f"After clearing rows: {full_rows}")
            print_grid(grid)

def adjust_grid(grid, column_heights, cleared_rows):
    # Build a mapping from old_row to new_row
    cleared_rows_set = set(cleared_rows)
    num_cleared = 0
    max_row = max(grid.keys()) if grid else -1
    row_mapping = {}
    for row in range(max_row + 1):
        if row in cleared_rows_set:
            # Mark this row for deletion
            continue
        # Determine how many cleared rows below
        num_cleared = sum(1 for cleared_row in cleared_rows if cleared_row < row)
        new_row = row - num_cleared
        row_mapping[row] = new_row

    # Update the grid in place
    rows_to_delete = set(grid.keys()) - set(row_mapping.keys())
    for old_row in list(grid.keys()):
        if old_row in rows_to_delete:
            del grid[old_row]
        else:
            new_row = row_mapping[old_row]
            if new_row != old_row:
                grid[new_row] = grid.pop(old_row)

    # Update column heights
    for col in range(10):
        # Find the highest occupied cell in the column
        occupied_rows = [row for row in grid if col in grid[row]]
        if occupied_rows:
            column_heights[col] = max(occupied_rows) + 1
        else:
            column_heights[col] = 0

def print_grid(grid):
    if not grid:
        print("(Grid is empty)")
        return
    max_row = max(grid.keys())
    for row in range(max_row, -1, -1):
        line = ''
        for col in range(10):
            if row in grid and col in grid[row]:
                line += grid[row][col]  # Display the shape letter
            else:
                line += '.'
        print(f"{row:2}: {line}")
    print("-" * 14)

def process_line(line, visualize=False):
    grid = {}  # row number -> dict of columns to shape letters
    column_heights = [0] * 10  # Heights of each column
    pieces = line.strip().split(',')

    for piece_entry in pieces:
        if not piece_entry:
            continue
        shape_letter = piece_entry[0]
        left_col = int(piece_entry[1:])
        shape_positions = SHAPES[shape_letter]

        # Drop the piece into the grid
        try:
            drop_piece(grid, column_heights, shape_letter, shape_positions, left_col, visualize=visualize)
        except ValueError as e:
            # Piece goes outside the grid or collision occurs; skip or handle as needed
            if visualize:
                print(f"Error: {e}")
            continue

    # Determine the final height
    if not grid:
        height = 0
    else:
        height = max(grid.keys()) + 1
    print(height)

def main():
    parser = argparse.ArgumentParser(description="Simplified Tetris Engine with Visualization")
    parser.add_argument('--visualize', action='store_true', help="Enable grid visualization after each piece is dropped")
    parser.add_argument('--print_shape', action='store_true', help="Print each shape")
    args = parser.parse_args()

    if args.print_shape:
        for shape_letter in SHAPES:
            print_shape(shape_letter)
        return

    lines = sys.stdin.read().splitlines()
    for line in lines:
        process_line(line, visualize=args.visualize)

if __name__ == "__main__":
    main()
