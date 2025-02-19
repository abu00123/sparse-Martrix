# Sparse Matrix Operations

## Overview
This project implements operations on sparse matrices, including addition, subtraction, and multiplication. A sparse matrix is a matrix where most elements are zero, and this implementation optimizes memory usage and computational efficiency.

## Features
- Reads two sparse matrices from an input file.
- Performs addition, subtraction, and multiplication.
- Implements an optimized data structure for sparse matrices.
- Provides exception handling for invalid input formats.
- Offers a command-line interface for selecting operations.

## Folder Structure
```
/dsa/sparse_matrix/
├── code/
│   ├── src/
│   │   ├── sparse_matrix.py  # Implementation of SparseMatrix class
│   │   ├── main.py  # Command-line interface for matrix operations
├── sample_inputs/
│   ├── matrix1.txt  # Sample sparse matrix input file
│   ├── matrix2.txt  # Sample sparse matrix input file
├── test/
│   ├── test_sparse_matrix.py  # Unit tests for SparseMatrix class
```

## Installation and Usage
### Prerequisites
Ensure you have Python installed (Python 3.x recommended).

### Running the Program
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sparse_matrix
   ```
2. Run the program:
   ```bash
   python code/src/main.py
   ```
3. Follow the command-line prompts to select operations.

### Running Tests
To run unit tests:
```bash
python -m unittest discover -s test -p "test_*.py"
```

## Input File Format
Each matrix file follows this format:
```
rows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)
...
```

## Exception Handling
- Ignores empty lines and extra whitespaces.
- Throws an error for invalid formats (e.g., missing values, incorrect parenthesis types).

## License
This project is open-source and available under the MIT License.
