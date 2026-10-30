# Correlation analysis project

## Goal
Check time series for Pearson correlation.

Data is provided in text files. `sample.txt` and `stock-short.txt` are example data files.
Data layout: every row represents one time series (for example, for one metric).
The data for time 0 is in the first column, time 1 in the second column, and so on.
All rows are expected to have the same number of entries. All entries are real numbers. Negative numbers and zeroes are possible.

Write a program that finds all pairs of time series (identified by their row indices) that have a Pearson correlation above
a threshold. The threshold is provided by the user when they call the program.

## General constraints
- Only read and write in this project directory and its subdirectories.
- Do not push to the `main` branch in git.

## Technology and tooling
- Python 3.12+ project
- No `pyproject.toml`, `src/`, or `tests/` exist yet; create them at the root when adding code.
- Use `uv` for dependency management if it is installed.

## Project structure
- All source code lives in `src/`.
- All tests live in `tests/`.

## Coding conventions
- Use **camelCase** for functions, classes, and variable names. (Do not default to Python snake_case.)
- Use named parameters in function definitions and calls where practical.

## Quality constraints
- Maintain test coverage of at least 70%.

## License constraints
- The project is under an Apache Commons License.
- Do not add dependencies incompatible with the Apache Commons License.
- Avoid dependencies with a GPL license.
