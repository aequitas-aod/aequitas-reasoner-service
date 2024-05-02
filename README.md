# Aequitas - Reasoner Service

## Prerequisites

- Python 3.10+

## Getting Started

- Run `pip install -r requirements.txt` to install poetry package manager.
- Run `poetry install` to install the project dependencies. Poetry will create a virtual environment that will be used
  to handle project dependencies.

## Dependencies Management

The purpose of [requirements](requirements.txt) file is just offering a quick way to install poetry.
Actual dependencies are managed by poetry itself.

You can add new dependencies to the project by running `poetry add <package-name>`. This will add the
package to the `pyproject.toml` file and install it in the virtual environment.

## Testing
In order to run the whole test suite:
  
```bash
poe test
```

If you want to run just unit tests:

```bash
poe unit-test
```

Or just integration tests:

```bash
poe intergation-test
```

## Code Style

This project uses [black](https://github.com/psf/black) code formatter.

### Check code style

```bash
poe format-check
```

### Format code

```bash
poe format
```