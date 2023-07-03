import cv2
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture(0)

def solve_sudoku(grid):
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True

    row, col = empty_cell

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row, col] = num

            if solve_sudoku(grid):
                return True

            grid[row, col] = 0

    return False

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i, j] == 0:
                return (i, j)
    return None

def is_safe(grid, row, col, num):
    # Check row
    if num in grid[row, :]:
        return False

    # Check column
    if num in grid[:, col]:
        return False

    # Check 3x3 box
    box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
    if num in grid[box_start_row:box_start_row + 3, box_start_col:box_start_col + 3]:
        return False

    return True

# Rest of the code (video capture and processing) remains the same.

while True:
    # Capture frame from video feed
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Preprocess the frame
    processed = cv2.GaussianBlur(gray, (9, 9), 0)
    processed = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the processed frame
    contours, _ = cv2.findContours(processed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Find the largest contour (presumably the Sudoku grid)
        largest_contour = max(contours, key=cv2.contourArea)

        # Extract the Sudoku grid from the frame
        x, y, w, h = cv2.boundingRect(largest_contour)
        sudoku_grid = processed[y:y + h, x:x + w]

        # # Resize the Sudoku grid to a fixed size (if necessary)
        # sudoku_grid = cv2.resize(sudoku_grid, (450, 450))

        # Determine the desired size for the Sudoku grid
        grid_size = 450

        # # Resize the Sudoku grid to a size that can be evenly divided into 9 cells
        # grid_height, grid_width = sudoku_grid.shape[:2]
        # resized_height = (grid_height // grid_size) * grid_size
        # resized_width = (grid_width // grid_size) * grid_size
        # sudoku_grid = cv2.resize(sudoku_grid, (resized_width, resized_height))

        # Resize the Sudoku grid to a size that can be evenly divided into 9 cells
        grid_height, grid_width = sudoku_grid.shape[:2]
        resized_height = int(grid_height / grid_size) * grid_size
        resized_width = int(grid_width / grid_size) * grid_size
        # sudoku_grid = cv2.resize(sudoku_grid, (resized_width, resized_height), interpolation=cv2.INTER_AREA)
        if resized_width > 0 and resized_height > 0:
            sudoku_grid = cv2.resize(sudoku_grid, (resized_width, resized_height), interpolation=cv2.INTER_AREA)
        else:
            continue



        # Prepare the Sudoku grid for digit extraction
        sudoku_grid = cv2.copyMakeBorder(sudoku_grid, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)

        # # Split the Sudoku grid into individual cells
        # cell_size = sudoku_grid.shape[0] // 9
        # cells = [np.hsplit(row, 9) for row in np.vsplit(sudoku_grid, 9)]

        # Split the Sudoku grid into individual cells
        rows, cols = 9, 9
        row_height, col_width = sudoku_grid.shape[:2]

        cell_height = row_height // rows
        cell_width = col_width // cols

        cells = [np.hsplit(row, cols) for row in np.vsplit(sudoku_grid, rows)]


        # Initialize an empty grid to store the Sudoku digits
        sudoku_digits = np.zeros((9, 9), dtype=int)

        # Extract and recognize digits in each cell of the Sudoku grid
        for i in range(9):
            for j in range(9):
                cell = cells[i][j]
                cell = cv2.bitwise_not(cell)  # Invert the cell to make digits black

                # Perform digit recognition on the cell (e.g., using OCR or custom algorithms)

                # Placeholder: Randomly assign a digit for demonstration purposes
                digit = np.random.randint(1, 10)
                sudoku_digits[i, j] = digit

        # Solve the Sudoku puzzle
        solve_sudoku(sudoku_digits)

        # Overlay the solution on the frame
        cell_size = frame.shape[0] // 9
        for i in range(9):
            for j in range(9):
                digit = sudoku_digits[i, j]
                if digit != 0:
                    cell_x = x + j * cell_size
                    cell_y = y + i * cell_size
                    cv2.putText(frame, str(digit), (cell_x + 30, cell_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    # Display the frame
    cv2.imshow('Real-Time Sudoku Solver', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
