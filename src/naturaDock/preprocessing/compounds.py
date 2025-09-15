# Compound Library Preprocessing

from pathlib import Path
from typing import Iterable, Iterator
from rdkit import Chem

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
    if file_ext == '.sdf':
        supplier = Chem.SDMolSupplier(str(library_path))
    elif file_ext in ['.smi', '.smiles']:
        supplier = Chem.SmilesMolSupplier(str(library_path), titleLine=False)
    elif file_ext == '.mol2':
        # RDKit's Mol2 parser can be less robust; this is a basic implementation.
        # For production, a more robust parser might be needed.
        mol = Chem.MolFromMol2File(str(library_path))
        supplier = [mol] if mol else []
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

    # Filter out None values in case of parsing errors
    return (mol for mol in supplier if mol is not None)

from rdkit.Chem import AllChem

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

from rdkit.Chem import Descriptors

def filter_compounds(molecules: Iterator[Chem.Mol], max_mol_weight: float = 500.0) -> Iterator[Chem.Mol]:
    """
    Filters molecules based on molecular weight.

    Args:
        molecules: An iterator of RDKit Mol objects.
        max_mol_weight: The maximum molecular weight allowed.

    Yields:
        RDKit Mol objects that pass the filter.
    """
    for mol in molecules:
        mol_weight = Descriptors.MolWt(mol)
        if mol_weight <= max_mol_weight:
            yield mol
