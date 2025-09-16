
import sys
from pathlib import Path


def get_meeko_path(script_name: str) -> Path:
    """
    Determines the absolute path to a Meeko script.

    Args:
        script_name: The name of the script (e.g., "mk_prepare_receptor.py").

    Returns:
        The absolute path to the script.

    Raises:
        FileNotFoundError: If the script cannot be found.
    """
    # Find the directory of the current Python executable
    python_executable = Path(sys.executable)
    scripts_dir = python_executable.parent / "Scripts"

    script_path = scripts_dir / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Meeko script '{script_name}' not found in '{scripts_dir}'")

    return script_path
