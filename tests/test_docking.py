import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

from naturaDock.docking.vina_dock import run_vina_docking

# Define test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
PROTEIN_PDBQT = TEST_DATA_DIR / "test_protein.pdbqt"
COMPOUND_PDBQT = TEST_DATA_DIR / "test_compound.pdbqt"
OUTPUT_PDBQT = TEST_DATA_DIR / "test_output.pdbqt"

BINDING_SITE = {
    "center_x": 15.0,
    "center_y": 15.0,
    "center_z": 15.0,
    "size_x": 20.0,
    "size_y": 20.0,
    "size_z": 20.0,
}

@patch('subprocess.run')
def test_run_vina_docking_success(mock_subprocess_run):
    """Test that the Vina command is constructed and executed correctly."""
    # Configure the mock to simulate a successful run
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Vina finished successfully", stderr=""
    )

    run_vina_docking(PROTEIN_PDBQT, COMPOUND_PDBQT, BINDING_SITE, OUTPUT_PDBQT)

    # Check that subprocess.run was called
    mock_subprocess_run.assert_called_once()

    # Check the command arguments
    args, kwargs = mock_subprocess_run.call_args
    command = args[0]
    assert str(PROTEIN_PDBQT) in command
    assert str(COMPOUND_PDBQT) in command
    assert str(OUTPUT_PDBQT) in command
    assert str(BINDING_SITE['center_x']) in command

@patch('subprocess.run')
def test_run_vina_docking_file_not_found(mock_subprocess_run):
    """Test that a FileNotFoundError is handled correctly."""
    # Configure the mock to raise FileNotFoundError
    mock_subprocess_run.side_effect = FileNotFoundError

    # The function should catch the exception and print an error
    with pytest.raises(FileNotFoundError):
        run_vina_docking(PROTEIN_PDBQT, COMPOUND_PDBQT, BINDING_SITE, OUTPUT_PDBQT)

@patch('subprocess.run')
def test_run_vina_docking_called_process_error(mock_subprocess_run):
    """Test that a CalledProcessError is handled correctly."""
    # Configure the mock to raise CalledProcessError
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="vina", output="error", stderr="error"
    )

    # The function should catch the exception and print an error
    with pytest.raises(subprocess.CalledProcessError):
        run_vina_docking(PROTEIN_PDBQT, COMPOUND_PDBQT, BINDING_SITE, OUTPUT_PDBQT)
