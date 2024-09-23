import sys
import argparse

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

def drop_piece(column_blocks, column_heights, shape_letter, shape_positions, left_col, row_counts, visualize=False):
    # Adjust the shape positions with the left_col
    adjusted_positions = [(row_offset, col_offset + left_col) for (row_offset, col_offset) in shape_positions]

    # Verify that all columns are within 0 to 9
    for row_offset, col in adjusted_positions:
        if col < 0 or col >= 10:
            raise ValueError("Piece goes outside the grid horizontally")

    # Determine the landing row based on column heights
    landing_row_candidates = [column_heights[col] - row_offset for row_offset, col in adjusted_positions]
    landing_row = max(landing_row_candidates)
    if landing_row < 0:
        landing_row = 0  # Ensure the piece does not go below the grid

    # Check for collision at the landing position
    for row_offset, col in adjusted_positions:
        row = landing_row + row_offset
        if row in column_blocks[col]:
            raise ValueError("Collision detected when placing the piece")

    new_rows = set()
    # Place the piece at landing_row + row_offset
    for row_offset, col in adjusted_positions:
        row = landing_row + row_offset

        column_blocks[col][row] = shape_letter  # Store the shape letter
        # Update column_heights
        if row + 1 > column_heights[col]:
            column_heights[col] = row + 1
        # Update row_counts
        row_counts[row] = row_counts.get(row, 0) + 1
        new_rows.add(row)
    if visualize:
        print("After dropping piece:")
        print_grid(column_blocks)
    # Check for full rows
    full_rows = check_full_rows(row_counts, new_rows)
    if full_rows:
        clear_rows(column_blocks, column_heights, row_counts, full_rows)
        if visualize:
            print(f"After clearing rows: {full_rows}")
            print_grid(column_blocks)

def check_full_rows(row_counts, rows_to_check):
    # Check only the newly occupied rows
    full_rows = [row for row in rows_to_check if row_counts.get(row, 0) == 10]
    return full_rows

def clear_rows(column_blocks, column_heights, row_counts, cleared_rows):
    cleared_rows_set = set(cleared_rows)
    new_row_counts = {}
    for col in range(10):
        # Get the list of rows in this column, sorted in ascending order
        rows_in_col = sorted(column_blocks[col].keys())
        new_blocks = {}
        num_cleared_below = 0
        for row in rows_in_col:
            if row in cleared_rows_set:
                # Remove this block
                # No need to update row_counts here
                num_cleared_below += 1
            else:
                # Shift down the block by num_cleared_below
                new_row = row - num_cleared_below
                new_blocks[new_row] = column_blocks[col][row]
                # Update new_row_counts for the new row
                new_row_counts[new_row] = new_row_counts.get(new_row, 0) + 1
        column_blocks[col] = new_blocks
        # Update column_heights
        if new_blocks:
            column_heights[col] = max(new_blocks.keys()) + 1
        else:
            column_heights[col] = 0
    # Update row_counts with new_row_counts
    row_counts.clear()
    row_counts.update(new_row_counts)

def print_grid(column_blocks):
    # Collect all occupied rows
    occupied_rows = set()
    for col in range(10):
        for row in column_blocks[col]:
            occupied_rows.add(row)
    if not occupied_rows:
        print("(Grid is empty)")
        return
    min_row = min(occupied_rows)
    max_row = max(occupied_rows)
    for row in range(max_row, min_row - 1, -1):
        line = ''
        for col in range(10):
            if row in column_blocks[col]:
                line += column_blocks[col][row]
            else:
                line += '.'
        print(f"{row:2}: {line}")
    print("-" * 14)

def process_line(line, visualize=False):
    column_blocks = [{} for _ in range(10)]
    column_heights = [0] * 10
    row_counts = {}  # Maintain a persistent row_counts dictionary
    pieces = line.strip().split(',')

    for piece_entry in pieces:
        if not piece_entry:
            continue
        shape_letter = piece_entry[0]
        left_col = int(piece_entry[1:])
        shape_positions = SHAPES[shape_letter]

        try:
            drop_piece(column_blocks, column_heights, shape_letter, shape_positions, left_col, row_counts, visualize=visualize)
        except ValueError as e:
            if visualize:
                print(f"Error: {e}")
            print('-1')
            return


    # Determine the final height
    occupied_rows = set()
    for col in range(10):
        occupied_rows.update(column_blocks[col].keys())
    if occupied_rows:
        height = max(occupied_rows) + 1
    else:
        height = 0
    print(height)

def main():
    parser = argparse.ArgumentParser(description="Optimized Tetris Engine with Visualization")
    parser.add_argument('--visualize', action='store_true', help="Enable grid visualization after each piece is dropped")
    args = parser.parse_args()

    lines = sys.stdin.read().splitlines()
    for line in lines:
        try:
            process_line(line, visualize=args.visualize)
        except Exception as e:
                    print("-1")

if __name__ == "__main__":
    main()
