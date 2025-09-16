# Compound Library Preprocessing

from pathlib import Path
from typing import Iterable, Iterator
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
import subprocess
from .utils.utils import get_meeko_path
import sys
import tempfile


def load_compounds(library_path: Path) -> Iterator[Chem.Mol]:
    """
    Loads a compound library from a file, supporting SDF, MOL2, and SMILES.

    Args:
        library_path: The file path to the compound library.

    Returns:
        An iterator of RDKit Mol objects.

    Raises:
        FileNotFoundError: If the library file does not exist.
        ValueError: If the file format is unsupported.
    """
    if not library_path.exists():
        raise FileNotFoundError(f"Compound library not found at: {library_path}")

    file_ext = library_path.suffix.lower()
    if file_ext == ".sdf":
        supplier = Chem.SDMolSupplier(str(library_path))
    elif file_ext in [".smi", ".smiles"]:
        supplier = Chem.SmilesMolSupplier(str(library_path), titleLine=False)
    elif file_ext == ".mol2":
        # RDKit's Mol2 parser can be less robust; this is a basic implementation.
        # For production, a more robust parser might be needed.
        mol = Chem.MolFromMol2File(str(library_path))
        supplier = [mol] if mol else []
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

    # Filter out None values in case of parsing errors
    return (mol for mol in supplier if mol is not None)


def generate_conformers(molecules: Iterator[Chem.Mol]) -> Iterator[Chem.Mol]:
    """
    Generates a 3D conformer for each molecule and optimizes its geometry.

    Args:
        molecules: An iterator of RDKit Mol objects.

    Yields:
        RDKit Mol objects with an embedded 3D conformer.
    """
    for mol in molecules:
        try:
            # Add hydrogens
            mol_with_hs = Chem.AddHs(mol)
            # Generate 3D conformer
            if AllChem.EmbedMolecule(mol_with_hs, randomSeed=42) == -1:
                # Conformer generation failed
                continue
            # Optimize the geometry
            if AllChem.UFFOptimizeMolecule(mol_with_hs) == -1:
                # Optimization failed
                continue
            yield mol_with_hs
        except Exception:
            # Skip molecules that fail for any reason during processing
            continue


def filter_compounds(
    molecules: Iterator[Chem.Mol],
    max_mol_weight: float = 500.0,
    max_rotatable_bonds: int = 10,
    min_logp: float = -5.0,
    max_logp: float = 5.0,
) -> Iterator[Chem.Mol]:
    """
    Filters molecules based on molecular weight, rotatable bonds, and logP.

    Args:
        molecules: An iterator of RDKit Mol objects.
        max_mol_weight: The maximum molecular weight allowed.
        max_rotatable_bonds: The maximum number of rotatable bonds allowed.
        min_logp: The minimum logP value allowed.
        max_logp: The maximum logP value allowed.

    Yields:
        RDKit Mol objects that pass the filters.
    """
    for mol in molecules:
        mol_weight = Descriptors.MolWt(mol)
        rotatable_bonds = Descriptors.NumRotatableBonds(mol)
        logp = Descriptors.MolLogP(mol)

        if (
            mol_weight <= max_mol_weight
            and rotatable_bonds <= max_rotatable_bonds
            and min_logp <= logp <= max_logp
        ):
            yield mol


def prepare_compounds(molecules: Iterable[Chem.Mol], output_dir: Path) -> list[Path]:
    """
    Prepares a list of compounds for docking, saving them as PDBQT files using Meeko.

    Args:
        molecules: A list of RDKit Mol objects.
        output_dir: The directory to save the PDBQT files.

    Returns:
        A list of Paths to the prepared PDBQT files.
    """
    prepared_paths = []
    mols = list(molecules)
    for i, mol in enumerate(mols):
        mol_name = (
            mol.GetProp("_Name")
            if mol.HasProp("_Name") and mol.GetProp("_Name")
            else f"compound_{i}"
        )
        output_path = output_dir / f"{mol_name}.pdbqt"

        tmp_file_path = None
        try:
            # Convert molecule to SDF format in memory
            sdf_data = Chem.MolToMolBlock(mol)

            with tempfile.NamedTemporaryFile(
                mode="w+", delete=False, suffix=".sdf"
            ) as tmp_file:
                tmp_file.write(sdf_data)
                tmp_file_path = tmp_file.name

            # Prepare command for Meeko
            script_path = get_meeko_path("mk_prepare_ligand.py")
            command = [
                sys.executable,
                str(script_path),
                "--mol",
                tmp_file_path,
                "-o",
                str(output_path),
            ]

            # Run Meeko
            result = subprocess.run(
                command, capture_output=True, text=True, check=True
            )

            if result.returncode == 0:
                prepared_paths.append(output_path)

        except subprocess.CalledProcessError as e:
            print(
                f"Warning: Failed to prepare molecule {mol_name}. "
                f"Error: {e.stderr}"
            )
            continue
        except Exception as e:
            print(f"Warning: An unexpected error occurred for molecule {mol_name}. Error: {e}")
            continue
        finally:
            # Clean up the temporary file
            if tmp_file_path and Path(tmp_file_path).exists():
                Path(tmp_file_path).unlink()

    return prepared_paths