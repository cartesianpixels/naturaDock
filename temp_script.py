import subprocess
import sys
from pathlib import Path

def get_meeko_path(script_name: str) -> Path:
    python_executable = Path(sys.executable)
    scripts_dir = python_executable.parent / "Scripts"
    script_path = scripts_dir / script_name
    if not script_path.exists():
        raise FileNotFoundError(
            f"Meeko script '{script_name}' not found in '{scripts_dir}'"
        )
    return script_path

script_path = get_meeko_path("mk_prepare_ligand.py")
command = ["python", str(script_path), "--help"]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)