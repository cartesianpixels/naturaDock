import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def generate_statistics(
    results_df: pd.DataFrame, output_dir: Path
):
    """Generates a statistical summary and a distribution plot of the docking scores.

    Args:
        results_df: DataFrame with the docking results.
        output_dir: Path to the directory to write the output files.
    """
    # Generate statistical summary
    summary = results_df["affinity"].describe()
    summary_path = output_dir / "statistical_summary.txt"
    with open(summary_path, "w") as f:
        f.write(summary.to_string())

    print(f"Statistical summary saved to {summary_path}")

    # Generate distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(results_df["affinity"], kde=True)
    plt.title("Distribution of Docking Scores")
    plt.xlabel("Binding Affinity (kcal/mol)")
    plt.ylabel("Frequency")
    plot_path = output_dir / "docking_scores_distribution.png"
    plt.savefig(plot_path)
    plt.close()

    print(f"Distribution plot saved to {plot_path}")
