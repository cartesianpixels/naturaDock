# AutoDock Vina Docking Execution

import subprocess
from pathlib import Path


import os

def run_vina_docking(
    protein_pdbqt: Path,
    compound_pdbqt: Path,
    binding_site: dict,
    output_pdbqt: Path,
):
    """
    Constructs and runs the AutoDock Vina docking command.

    Args:
        protein_pdbqt: Path to the prepared protein file in PDBQT format.
        compound_pdbqt: Path to the prepared compound file in PDBQT format.
        binding_site: Dictionary defining the docking box (center and size).
        output_pdbqt: Path to write the docked pose output file.
    """
    # Get Vina executable path from environment variable or use default
    vina_executable = os.environ.get("VINA_EXECUTABLE", Path("vina.exe").resolve())


    command = [
        str(vina_executable),
        "--receptor",
        str(protein_pdbqt),
        "--ligand",
        str(compound_pdbqt),
        "--out",
        str(output_pdbqt),
        "--center_x",
        str(binding_site["center_x"]),
        "--center_y",
        str(binding_site["center_y"]),
        "--center_z",
        str(binding_site["center_z"]),
        "--size_x",
        str(binding_site["size_x"]),
        "--size_y",
        str(binding_site["size_y"]),
        "--size_z",
        str(binding_site["size_z"]),
        "--cpu",
        "1",  # Example: Use 1 CPU core
    ]

    print(f"Executing Vina Command: {' '.join(command)}")

    # Placeholder for actual execution
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Vina stdout:", result.stdout)
        print("Vina stderr:", result.stderr)
    except FileNotFoundError:
        print(
            f"Error: '{vina_executable}' not found. "
            "Please ensure AutoDock Vina is installed and in your PATH."
        )
    except subprocess.CalledProcessError as e:
        print(f"Vina execution failed with exit code {e.returncode}")
        print("Vina stdout:", e.stdout)
        print("Vina stderr:", e.stderr)

    # This function would typically return the path to the output file or parse scores.
    return output_pdbqt
