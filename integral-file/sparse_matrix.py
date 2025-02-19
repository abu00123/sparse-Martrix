import os

class SparseMatrix:
    def __init__(self, rows=0, cols=0, data=None):
        """
        Initialize a sparse matrix.
        :param rows: Number of rows.
        :param cols: Number of columns.
        :param data: Dictionary to store non-zero elements.
        """
        self.rows = rows
        self.cols = cols
        self.data = data if data else {}

    @staticmethod
    def load_from_file(file_path):
        """
        Load a sparse matrix from a file.
        :param file_path: Path to the input file.
        :return: SparseMatrix object.
        """
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            # Parse metadata
            rows = int(lines[0].split('=')[1].strip())
            cols = int(lines[1].split('=')[1].strip())
            data = {}

            # Parse entries
            for line in lines[2:]:
                if not line.startswith('(') or not line.endswith(')'):
                    raise ValueError("Invalid format: Parentheses expected.")

                entry = line[1:-1].split(',')
                if len(entry) != 3:
                    raise ValueError("Invalid format: Expected (row, col, value).")

                row, col, value = map(str.strip, entry)
                if not row.isdigit() or not col.isdigit():
                    raise ValueError("Invalid format: Row and column indices must be integers.")
                if not value.lstrip('-').isdigit():
                    raise ValueError("Invalid format: Value must be an integer.")

                data[(int(row), int(col))] = int(value)

            return SparseMatrix(rows, cols, data)

        except Exception as e:
            raise ValueError(f"Input file has wrong format: {str(e)}")

    def getElement(self, row, col):
        """
        Get the element at (row, col).
        :param row: Row index.
        :param col: Column index.
        :return: Element value.
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Index out of bounds.")
        return self.data.get((row, col), 0)

    def setElement(self, row, col, value):
        """
        Set the element at (row, col).
        :param row: Row index.
        :param col: Column index.
        :param value: Value to set.
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Index out of bounds.")
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def add(self, other):
        """
        Add two sparse matrices.
        :param other: Another SparseMatrix object.
        :return: Resultant SparseMatrix object.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result_data = self.data.copy()
        for key, value in other.data.items():
            if key in result_data:
                result_data[key] += value
                if result_data[key] == 0:
                    del result_data[key]
            else:
                result_data[key] = value

        return SparseMatrix(self.rows, self.cols, result_data)

    def subtract(self, other):
        """
        Subtract two sparse matrices.
        :param other: Another SparseMatrix object.
        :return: Resultant SparseMatrix object.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result_data = self.data.copy()
        for key, value in other.data.items():
            if key in result_data:
                result_data[key] -= value
                if result_data[key] == 0:
                    del result_data[key]
            else:
                result_data[key] = -value

        return SparseMatrix(self.rows, self.cols, result_data)

    def multiply(self, other):
        """
        Multiply two sparse matrices.
        :param other: Another SparseMatrix object.
        :return: Resultant SparseMatrix object.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix.")

        result_rows, result_cols = self.rows, other.cols
        result_data = {}

        # Iterate through all non-zero elements of the first matrix
        for (i, k), val1 in self.data.items():
            for j in range(result_cols):
                val2 = other.getElement(k, j)
                if val2 != 0:
                    result_key = (i, j)
                    result_data[result_key] = result_data.get(result_key, 0) + val1 * val2
                    if result_data[result_key] == 0:
                        del result_data[result_key]

        return SparseMatrix(result_rows, result_cols, result_data)

    def save_to_file(self, file_path):
        """
        Save the sparse matrix to a file.
        :param file_path: Path to the output file.
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for (row, col), value in self.data.items():
                f.write(f"({row}, {col}, {value})\n")


# Main program
if __name__ == "__main__":
    print("Sparse Matrix Operations")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    choice = input("Select operation (1/2/3): ")

    file1 = input("Enter path to the first matrix file: ")
    file2 = input("Enter path to the second matrix file: ")

    try:
        matrix1 = SparseMatrix.load_from_file(file1)
        matrix2 = SparseMatrix.load_from_file(file2)

        if choice == '1':
            result = matrix1.add(matrix2)
            output_file = "output/add_result.txt"
        elif choice == '2':
            result = matrix1.subtract(matrix2)
            output_file = "output/subtract_result.txt"
        elif choice == '3':
            result = matrix1.multiply(matrix2)
            output_file = "output/multiply_result.txt"
        else:
            print("Invalid choice.")
            exit()

        result.save_to_file(output_file)
        print(f"Result saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
