from pathlib import Path
import subprocess
import pandas as pd
import os

# Define test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
PROTEIN_PDB = TEST_DATA_DIR / "test_protein.pdb"
COMPOUND_SDF = TEST_DATA_DIR / "test_compounds_small.sdf"
OUTPUT_DIR = Path(__file__).parent / "cli_output"


def test_cli_workflow():
    """Test the full CLI workflow from preprocessing to analysis."""
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
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")

    result = subprocess.run(command, capture_output=True, text=True, env=env)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.returncode == 0, f"CLI test failed with stderr:\n{result.stderr}"
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
    assert len(prepared_files) == 2

    docked_files = list(docking_results_dir.glob("*.pdbqt"))
    assert len(docked_files) == 2

    # Check analysis output
    ranked_csv = OUTPUT_DIR / "ranked_results.csv"
    assert ranked_csv.exists()

    df = pd.read_csv(ranked_csv)
    assert len(df) == 2
    assert "compound" in df.columns
    assert "affinity" in df.columns
    assert all(df["affinity"] <= 0)

    summary_path = OUTPUT_DIR / "statistical_summary.txt"
    assert summary_path.exists()

    plot_path = OUTPUT_DIR / "docking_scores_distribution.png"
    assert plot_path.exists()

    # Clean up output directory
    subprocess.run(["rmdir", "/s", "/q", str(OUTPUT_DIR)], shell=True)
