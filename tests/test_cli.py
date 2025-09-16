from pathlib import Path
import subprocess

# Define test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
PROTEIN_PDB = TEST_DATA_DIR / "test_protein.pdb"
COMPOUND_SDF = TEST_DATA_DIR / "test_compounds.sdf"
OUTPUT_DIR = Path(__file__).parent / "cli_output"


def test_cli():
    """Test the full CLI workflow."""
    # Ensure output directory is clean
    if OUTPUT_DIR.exists():
        subprocess.run(["rmdir", "/s", "/q", str(OUTPUT_DIR)], shell=True)
    OUTPUT_DIR.mkdir()

    command = [
        "python",
        "src/naturaDock/main.py",
        "-p",
        str(PROTEIN_PDB),
        "-l",
        str(COMPOUND_SDF),
        "-o",
        str(OUTPUT_DIR),
        "--center_x",
        "15.0",
        "--center_y",
        "15.0",
        "--center_z",
        "15.0",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    assert result.returncode == 0
    assert "naturaDock pipeline finished" in result.stdout

    # Check for output files
    protein_pdbqt = OUTPUT_DIR / "test_protein.pdbqt"
    assert protein_pdbqt.exists()

    prepared_compounds_dir = OUTPUT_DIR / "prepared_compounds"
    assert prepared_compounds_dir.exists()

    docking_results_dir = OUTPUT_DIR / "docking_results"
    assert docking_results_dir.exists()

    # Check if at least one compound was prepared and docked
    prepared_files = list(prepared_compounds_dir.glob("*.pdbqt"))
    assert len(prepared_files) > 0

    docked_files = list(docking_results_dir.glob("*.pdbqt"))
    assert len(docked_files) > 0
