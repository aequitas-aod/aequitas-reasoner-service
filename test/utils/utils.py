from pathlib import Path


def get_file_path(relative_path) -> Path:
    """Helper method to get the absolute path of the YAML file."""
    current_file = Path(__file__).resolve()
    root_dir = current_file.parents[2]
    return root_dir / relative_path
