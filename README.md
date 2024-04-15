# Prolog Implementation With Python

## Course: CSC14003 - Artificial Intelligence

This repository contains an ongoing project to implement Prolog functionality using Python. Prolog is a logic programming language that is particularly well-suited for symbolic and symbolic computation tasks. This implementation aims to provide a Python-based interpreter for Prolog programs, allowing users to leverage Prolog's logical inference capabilities within Python applications.


## Status

**Note:** This implementation is currently incomplete and is under development.

## Features

- Basic Prolog syntax parsing
- Limited support for Prolog predicates and rules
- Integration with Python code

## Usage

To use this Prolog implementation within your Python project, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/prolog-implementation-with-python.git
   ```

2. Navigate to the project directory:

   ```bash
   cd prolog-implementation-with-python
   ```

3. Import the `prolog` module into your Python code:

   ```python
   import prolog
   ```

4. Start writing Prolog-like logic using Python syntax.

## Example

Here's a simple example of using this Prolog implementation within Python:

```python
import prolog

# Define some Prolog-like rules
prolog.rules = [
    "father(john, bob)",
    "father(bob, alice)",
    "mother(ann, alice)"
]

# Query the knowledge base
result = prolog.query("father(X, alice)")

# Print the result
for res in result:
    print(res)
```

This would output:

```
{'X': 'bob'}
```

## Contributing

Contributions are highly encouraged! If you'd like to contribute to this project, please feel free to submit pull requests, report issues, or suggest improvements.

Feel free to adjust the content and formatting according to your preferences and project requirements!
