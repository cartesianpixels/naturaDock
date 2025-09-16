from pathlib import Path
from naturaDock.preprocessing.compounds import load_compounds, generate_conformers, filter_compounds, prepare_compounds
from rdkit import Chem

TEST_DATA_DIR = Path(__file__).parent / "data"
COMPOUND_SDF = TEST_DATA_DIR / "test_compounds.sdf"

def test_load_compounds():
    compounds = list(load_compounds(COMPOUND_SDF))
    assert len(compounds) == 1
    assert isinstance(compounds[0], Chem.Mol)
    assert compounds[0].GetNumAtoms() == 6 # Benzene has 6 carbon atoms

def test_generate_conformers():
    compounds = list(load_compounds(COMPOUND_SDF))
    conformers = list(generate_conformers(iter(compounds)))
    assert len(conformers) == 1
    assert conformers[0].GetNumConformers() > 0
