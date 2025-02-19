class SparseMatrix:
    def __init__(self, rows=0, cols=0):
        """
        Initialize a sparse matrix with given dimensions.
        :param rows: Number of rows in the matrix.
        :param cols: Number of columns in the matrix.
        """
        self.rows = rows
        self.cols = cols
        self.data = {}  # Dictionary to store non-zero elements

    @staticmethod
    def readFile(filePath):
        """
        Reads a sparse matrix from a file.
        :param filePath: Path to the input file.
        :return: A SparseMatrix object.
        """
        try:
            with open(filePath, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]  # Ignore empty lines

            # Parse number of rows and columns
            if len(lines) < 2:
                raise ValueError("Input file must have at least two lines for rows and cols.")
            
            rows_line = lines[0].split('=')
            cols_line = lines[1].split('=')
            if len(rows_line) != 2 or len(cols_line) != 2:
                raise ValueError("Invalid format for rows or cols definition.")
            
            rows = int(rows_line[1])
            cols = int(cols_line[1])

            matrix = SparseMatrix(rows, cols)

            # Parse matrix entries
            for line in lines[2:]:
                if not line.startswith('(') or not line.endswith(')'):
                    raise ValueError(f"Invalid format: Expected '(row, col, value)', got {line}")
                
                parts = line[1:-1].split(',')
                if len(parts) != 3:
                    raise ValueError(f"Invalid format: Expected three values, got {parts}")
                
                row, col, value = map(int, parts)
                if row >= rows or col >= cols:
                    raise ValueError(f"Index out of bounds: ({row}, {col})")
                
                matrix.setElement(row, col, value)
            return matrix
        except Exception as e:
            print(f"Error reading file: {e}")
            raise ValueError("Input file has wrong format")

    def getElement(self, row, col):
        """
        Retrieve the value at a specific position.
        :param row: Row index.
        :param col: Column index.
        :return: Value at (row, col), defaulting to 0 if not present.
        """
        return self.data.get((row, col), 0)

    def setElement(self, row, col, value):
        """
        Set the value at a specific position.
        :param row: Row index.
        :param col: Column index.
        :param value: Value to set.
        """
        if value == 0:
            if (row, col) in self.data:
                del self.data[(row, col)]
        else:
            self.data[(row, col)] = value

    def add(self, other):
        """
        Add two sparse matrices.
        :param other: Another SparseMatrix object.
        :return: A new SparseMatrix representing the sum.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")
        
        result = SparseMatrix(self.rows, self.cols)
        for pos in self.data:
            result.setElement(pos[0], pos[1], self.data[pos] + other.getElement(pos[0], pos[1]))
        for pos in other.data:
            if pos not in self.data:
                result.setElement(pos[0], pos[1], other.data[pos])
        
        return result

    def subtract(self, other):
        """
        Subtract two sparse matrices.
        :param other: Another SparseMatrix object.
        :return: A new SparseMatrix representing the difference.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")
        
        result = SparseMatrix(self.rows, self.cols)
        for pos in self.data:
            result.setElement(pos[0], pos[1], self.data[pos] - other.getElement(pos[0], pos[1]))
        for pos in other.data:
            if pos not in self.data:
                result.setElement(pos[0], pos[1], -other.data[pos])
        
        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices.
        :param other: Another SparseMatrix object.
        :return: A new SparseMatrix representing the product.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix.")
        
        result = SparseMatrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                total = 0
                for k in range(self.cols):
                    total += self.getElement(i, k) * other.getElement(k, j)
                if total != 0:
                    result.setElement(i, j, total)
        
        return result

    def writeToFile(self, outputPath):
        """
        Write the sparse matrix to a file.
        :param outputPath: Path to the output file.
        """
        with open(outputPath, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (row, col), value in self.data.items():
                file.write(f"({row}, {col}, {value})\n")


# Main Program
if __name__ == "__main__":
    # Predefined matrix file paths
    matrix_files = {
        "1": "sample_inputs/matrix1.txt",
        "2": "sample_inputs/matrix2.txt"
    }

    # Ensure Results directory exists (without using os)
    results_dir = "Results"
    try:
        # Check if the Results directory exists
        with open(f"{results_dir}/.placeholder", 'w'):  # Create a placeholder file to test directory existence
            pass
    except FileNotFoundError:
        # If it doesn't exist, create it manually
        with open(f"{results_dir}/.placeholder", 'w'):  # Create the directory by creating a placeholder file
            pass

    # User Input for Matrices
    print("Welcome to the Sparse Matrix Operations Program!")
    print("Select the first matrix:")
    print("1. matrix1.txt")
    print("2. matrix2.txt")
    choice1 = input("Enter your choice (1/2): ").strip()
    if choice1 not in ["1", "2"]:
        print("Invalid choice for the first matrix. Please enter 1 or 2.")
        exit(1)

    print("\nSelect the second matrix:")
    print("1. matrix1.txt")
    print("2. matrix2.txt")
    choice2 = input("Enter your choice (1/2): ").strip()
    if choice2 not in ["1", "2"]:
        print("Invalid choice for the second matrix. Please enter 1 or 2.")
        exit(1)

    # Load matrices
    try:
        matrix1_path = matrix_files[choice1]
        matrix2_path = matrix_files[choice2]
        matrix1 = SparseMatrix.readFile(matrix1_path)
        matrix2 = SparseMatrix.readFile(matrix2_path)
    except ValueError as ve:
        print(f"Error loading matrices: {ve}")
        exit(1)

    # User Input for Operation
    print("\nSelect an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    if choice not in ["1", "2", "3"]:
        print("Invalid choice. Please enter 1, 2, or 3.")
        exit(1)

    try:
        # Perform operation
        if choice == "1":
            result = matrix1.add(matrix2)
            operation_name = "Addition"
            output_file = f"{results_dir}/add_result.txt"
        elif choice == "2":
            result = matrix1.subtract(matrix2)
            operation_name = "Subtraction"
            output_file = f"{results_dir}/subtract_result.txt"
        elif choice == "3":
            result = matrix1.multiply(matrix2)
            operation_name = "Multiplication"
            output_file = f"{results_dir}/multiply_result.txt"

        # Write result to file
        result.writeToFile(output_file)
        print(f"{operation_name} completed successfully. Output written to {output_file}.")
    except ValueError as ve:
        print(f"Error performing operation: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
