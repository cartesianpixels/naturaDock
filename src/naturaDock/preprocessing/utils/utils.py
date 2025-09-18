import sys
from pathlib import Path

def get_meeko_path(script_name: str) -> Path:
    python_executable = Path(sys.executable)
    
    if sys.platform == "win32":
        scripts_dir = python_executable.parent / "Scripts"
    else:
        # On Linux: /usr/local/bin/python -> go up to /usr/local, then into bin
        scripts_dir = python_executable.parent
    
    script_path = scripts_dir / script_name
    if not script_path.exists():
        raise FileNotFoundError(
            f"Meeko script '{script_name}' not found in '{scripts_dir}'"
        )
    return script_path