# Aequitas - Reasoner Service

## Prerequisites

- Python 3.8+

## Getting Started

- Run `pip install -r requirements.txt` to install poetry package manager.
- Run `poetry install` to install the project dependencies. Poetry will create a virtual environment that will be used
  to handle project dependencies.

## Dependencies Management

The purpose of [requirements](requirements.txt) file is only to offer a quick way to install poetry.
Actual dependencies are managed by poetry itself.

You can add new dependencies to the project by running `poetry add <package-name>`. This will add the
package to the `pyproject.toml` file and install it in the virtual environment.

## Code Style

This project uses [black](https://github.com/psf/black) code formatter.

### Check code style

```bash
poetry run black --check .
```

### Format code

```bash
poetry run black .
```