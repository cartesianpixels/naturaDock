# Protein Preprocessing

from pathlib import Path
from Bio.PDB import PDBParser, PDBExceptions
from pdbfixer import PDBFixer
import subprocess
from .utils.utils import get_meeko_path
import sys


def load_protein(protein_pdb_path: Path):
    """
    Loads a protein from a PDB file, performs validation, and returns a structure object.

    Args:
        protein_pdb_path: The file path to the protein's PDB file.

    Returns:
        A Bio.PDB.Structure object.

    Raises:
        FileNotFoundError: If the PDB file does not exist.
        ValueError: If the PDB file is malformed or cannot be parsed.
    """
    if not protein_pdb_path.exists():
        raise FileNotFoundError(f"PDB file not found at: {protein_pdb_path}")

    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure(protein_pdb_path.stem, str(protein_pdb_path))
        return structure
    except PDBExceptions.PDBConstructionException as e:
        raise ValueError(
            f"Failed to parse PDB file {protein_pdb_path}. "
            f"It may be malformed. Error: {e}"
        )


def define_binding_site(
    center_x: float,
    center_y: float,
    center_z: float,
    size_x: float = 20.0,
    size_y: float = 20.0,
    size_z: float = 20.0,
) -> dict:
    """
    Creates a dictionary defining the center and size of the docking box.

    This information is used by AutoDock Vina to specify the search space for docking.

    Args:
        center_x: The x-coordinate of the center of the box.
        center_y: The y-coordinate of the center of the box.
        center_z: The z-coordinate of the center of the box.
        size_x: The size of the box in the x-dimension (in Angstroms).
        size_y: The size of the box in the y-dimension (in Angstroms).
        size_z: The size of the box in the z-dimension (in Angstroms).

    Returns:
        A dictionary containing the binding site parameters.
    """
    return {
        "center_x": center_x,
        "center_y": center_y,
        "center_z": center_z,
        "size_x": size_x,
        "size_y": size_y,
        "size_z": size_z,
    }


def validate_protein(protein_pdb_path: Path) -> dict:
    """
    Validates a protein PDB file for common issues.

    Args:
        protein_pdb_path: The file path to the protein's PDB file.

    Returns:
        A dictionary containing validation results.
    """
    fixer = PDBFixer(str(protein_pdb_path))
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    fixer.findMissingAtoms()

    validation_results = {
        "missing_residues": fixer.missingResidues,
        "nonstandard_residues": fixer.nonstandardResidues,
        "missing_atoms": fixer.missingAtoms,
    }

    print("Protein Validation Results:")
    print(f"  Missing Residues: {len(validation_results['missing_residues'])}")
    print(
        f"  Non-standard Residues: {len(validation_results['nonstandard_residues'])}"
    )
    print(f"  Missing Atoms: {len(validation_results['missing_atoms'])}")

    return validation_results


def prepare_protein(protein_pdb_path: Path, protein_pdbqt_path: Path):
    """
    Prepares a protein for docking by converting it to PDBQT format using Meeko.

    Args:
        protein_pdb_path: The file path to the protein's PDB file.
        protein_pdbqt_path: The file path to write the PDBQT file.

    Raises:
        RuntimeError: If the Meeko script fails.
    """
    script_path = get_meeko_path("mk_prepare_receptor.py")
    command = [
        "python",
        str(script_path),
        "--pdb",
        str(protein_pdb_path),
        "-o",
        str(protein_pdbqt_path),
        "--skip_gpf",
    ]

    print(f"Executing Meeko for protein: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Meeko stdout:", result.stdout)
        print("Meeko stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Meeko protein preparation failed with exit code {e.returncode}\n"
            f"Stderr: {e.stderr}"
        )