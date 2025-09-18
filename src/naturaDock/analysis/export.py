import pandas as pd
from pathlib import Path

def rank_and_export_results(
    results_df: pd.DataFrame, output_dir: Path, format: str = "csv"
):
    """Ranks the results by affinity and exports them to a file.

    Args:
        results_df: DataFrame with the docking results.
        output_dir: Path to the directory to write the output file.
        format: The output format, either "csv" or "xlsx".
    """
    ranked_df = results_df.sort_values(by="affinity").reset_index(drop=True)

    if format == "csv":
        output_path = output_dir / "ranked_results.csv"
        ranked_df.to_csv(output_path, index=False)
    elif format == "xlsx":
        output_path = output_dir / "ranked_results.xlsx"
        ranked_df.to_excel(output_path, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")

    print(f"Ranked results exported to {output_path}")
