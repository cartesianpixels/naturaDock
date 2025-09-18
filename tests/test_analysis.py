import pytest
from pathlib import Path
import pandas as pd

from naturaDock.analysis.results import parse_vina_result, aggregate_results
from naturaDock.analysis.export import rank_and_export_results
from naturaDock.analysis.statistics import generate_statistics

# Define test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
RESULTS_DIR = TEST_DATA_DIR / "results"

@pytest.fixture(scope="module")
def dummy_results_dir(tmpdir_factory):
    """Create a dummy results directory with some PDBQT files."""
    results_dir = tmpdir_factory.mktemp("results")
    (results_dir / "compound1_docked.pdbqt").write_text(
        "REMARK VINA RESULT: -7.5 0.000 0.000", encoding="utf-8"
    )
    (results_dir / "compound2_docked.pdbqt").write_text(
        "REMARK VINA RESULT: -8.2 0.000 0.000", encoding="utf-8"
    )
    (results_dir / "compound3_docked.pdbqt").write_text(
        "Invalid PDBQT file", encoding="utf-8"
    )
    return Path(str(results_dir))

def test_parse_vina_result():
    """Test parsing a Vina output PDBQT file."""
    pdbqt_file = RESULTS_DIR / "compound1_docked.pdbqt"
    pdbqt_file.parent.mkdir(exist_ok=True)
    pdbqt_file.write_text("REMARK VINA RESULT: -7.5 0.000 0.000", encoding="utf-8")
    affinity = parse_vina_result(pdbqt_file)
    assert affinity == -7.5

def test_aggregate_results(dummy_results_dir):
    """Test aggregating results from a directory."""
    results_df = aggregate_results(dummy_results_dir)
    assert isinstance(results_df, pd.DataFrame)
    assert len(results_df) == 2
    assert "compound" in results_df.columns
    assert "affinity" in results_df.columns

def test_rank_and_export_results(dummy_results_dir):
    """Test ranking and exporting results."""
    results_df = aggregate_results(dummy_results_dir)
    output_dir = dummy_results_dir

    # Test CSV export
    rank_and_export_results(results_df, output_dir, format="csv")
    csv_output = output_dir / "ranked_results.csv"
    assert csv_output.exists()
    df = pd.read_csv(csv_output)
    assert df.iloc[0]["compound"] == "compound2"

    # Test XLSX export
    rank_and_export_results(results_df, output_dir, format="xlsx")
    xlsx_output = output_dir / "ranked_results.xlsx"
    assert xlsx_output.exists()
    df = pd.read_excel(xlsx_output)
    assert df.iloc[0]["compound"] == "compound2"

def test_generate_statistics(dummy_results_dir):
    """Test generating statistics."""
    results_df = aggregate_results(dummy_results_dir)
    output_dir = dummy_results_dir

    generate_statistics(results_df, output_dir)

    summary_path = output_dir / "statistical_summary.txt"
    assert summary_path.exists()

    plot_path = output_dir / "docking_scores_distribution.png"
    assert plot_path.exists()
