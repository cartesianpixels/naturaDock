# AutoDock Vina Docking Execution
import subprocess
import shutil
import os
from pathlib import Path


def get_vina_executable() -> str:
    """
    Finds the AutoDock Vina executable, checking in order:
    1. VINA_EXECUTABLE environment variable
    2. System PATH (works on Linux/Mac after apt/brew install)
    3. vina.exe in the project root (Windows local install)
    """
    # 1. Environment variable override
    if "VINA_EXECUTABLE" in os.environ:
        return os.environ["VINA_EXECUTABLE"]

    # 2. System PATH
    vina = shutil.which("vina")
    if vina:
        return vina

    # 3. Windows fallback - vina.exe next to project root
    local = Path(__file__).parent.parent.parent / "vina.exe"
    if local.exists():
        return str(local)

    raise FileNotFoundError(
        "AutoDock Vina not found. Install it, add it to PATH, "
        "or set the VINA_EXECUTABLE environment variable."
    )


def run_vina_docking(
    protein_pdbqt: Path,
    compound_pdbqt: Path,
    binding_site: dict,
    output_pdbqt: Path,
):
    """
    Constructs and runs the AutoDock Vina docking command.
    """
    vina_executable = get_vina_executable()

    command = [
        vina_executable,
        "--receptor", str(protein_pdbqt),
        "--ligand", str(compound_pdbqt),
        "--out", str(output_pdbqt),
        "--center_x", str(binding_site["center_x"]),
        "--center_y", str(binding_site["center_y"]),
        "--center_z", str(binding_site["center_z"]),
        "--size_x", str(binding_site["size_x"]),
        "--size_y", str(binding_site["size_y"]),
        "--size_z", str(binding_site["size_z"]),
        "--cpu", "1",
    ]

    print(f"Executing Vina command: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Vina stdout:", result.stdout)
        print("Vina stderr:", result.stderr)
        return result
    except FileNotFoundError:
        print(
            f"Error: '{vina_executable}' not found. "
            "Please ensure AutoDock Vina is installed and in your PATH."
        )
        raise
    except subprocess.CalledProcessError as e:
        print(f"Vina execution failed with exit code {e.returncode}")
        print("Vina stdout:", e.stdout)
        print("Vina stderr:", e.stderr)
        raise