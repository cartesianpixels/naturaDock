from pathlib import Path
import pandas as pd

def parse_vina_result(pdbqt_file: Path) -> float:
    """Parses a Vina output PDBQT file to extract the binding affinity.

    Args:
        pdbqt_file: Path to the Vina output PDBQT file.

    Returns:
        The binding affinity in kcal/mol, or None if not found.
    """
    with open(pdbqt_file, "r") as f:
        for line in f:
            if line.startswith("REMARK VINA RESULT:"):
                return float(line.split()[3])
    return None

def aggregate_results(results_dir: Path) -> pd.DataFrame:
    """Aggregates docking results from a directory.

    Args:
        results_dir: Path to the directory containing docking results.

    Returns:
        A pandas DataFrame with the aggregated results.
    """
    results = []
    for pdbqt_file in results_dir.glob("*_docked.pdbqt"):
        compound_name = pdbqt_file.stem.replace("_docked", "")
        affinity = parse_vina_result(pdbqt_file)
        if affinity is not None:
            results.append({"compound": compound_name, "affinity": affinity})
    
    return pd.DataFrame(results)
