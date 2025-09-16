import pytest
from pathlib import Path
from rdkit import Chem
from Bio.PDB.Structure import Structure

from naturaDock.preprocessing.protein import load_protein, validate_protein
from naturaDock.preprocessing.compounds import (
    load_compounds,
    generate_conformers,
    filter_compounds,
)

# Define test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
VALID_PDB = TEST_DATA_DIR / "test_protein.pdb"
VALID_SDF = TEST_DATA_DIR / "test_compounds.sdf"
NON_EXISTENT_FILE = TEST_DATA_DIR / "non_existent.file"

# --- Protein Loading Tests ---


def test_load_protein_success():
    """Test that a valid PDB file loads correctly."""
    structure = load_protein(VALID_PDB)
    assert isinstance(structure, Structure)
    assert structure.id == "test_protein"


def test_load_protein_file_not_found():
    """Test that a FileNotFoundError is raised for a non-existent PDB file."""
    with pytest.raises(FileNotFoundError):
        load_protein(NON_EXISTENT_FILE)


def test_validate_protein_success():
    """Test that a valid PDB file is validated correctly."""
    validation_results = validate_protein(VALID_PDB)
    assert isinstance(validation_results, dict)
    assert "missing_residues" in validation_results
    assert "nonstandard_residues" in validation_results
    assert "missing_atoms" in validation_results


# --- Compound Loading Tests ---


def test_load_compounds_sdf_success():
    """Test that a valid SDF file loads correctly."""
    molecules = list(load_compounds(VALID_SDF))
    assert len(molecules) == 1
    assert isinstance(molecules[0], Chem.Mol)
    assert molecules[0].GetNumAtoms() == 6 # Benzene has 6 carbon atoms


def test_load_compounds_file_not_found():
    """Test that a FileNotFoundError is raised for a non-existent library file."""
    with pytest.raises(FileNotFoundError):
        load_compounds(NON_EXISTENT_FILE)


def test_load_compounds_unsupported_format():
    """Test that a ValueError is raised for an unsupported file format."""
    # Create a dummy file with an unsupported extension
    unsupported_file = TEST_DATA_DIR / "test.txt"
    unsupported_file.touch()
    with pytest.raises(ValueError):
        load_compounds(unsupported_file)
    unsupported_file.unlink()  # Clean up the dummy file


# --- Compound Processing Tests ---


def test_generate_conformers_success():
    """Test that a 3D conformer is successfully generated."""
    mol = Chem.MolFromSmiles("C")  # Methane
    processed_mols = list(generate_conformers([mol]))
    assert len(processed_mols) == 1
    assert processed_mols[0].GetNumConformers() > 0


def test_filter_compounds_logic():
    """Test that the molecular weight filter works correctly."""
    # Methane (~16) and Iodine (~127)
    mol_light = Chem.MolFromSmiles("C")
    mol_heavy = Chem.MolFromSmiles("I")
    molecules = [mol_light, mol_heavy]

    filtered_list = list(filter_compounds(molecules, max_mol_weight=100.0))

    assert len(filtered_list) == 1
    # Check that the remaining molecule is methane
    assert filtered_list[0].GetNumAtoms() == 1
    assert filtered_list[0].GetAtomWithIdx(0).GetSymbol() == "C"
