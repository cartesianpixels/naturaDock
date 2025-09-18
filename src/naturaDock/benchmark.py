
import pandas as pd
from sklearn.metrics import roc_auc_score

def calculate_enrichment_factor(
    df: pd.DataFrame, active_column: str, score_column: str, percentile: float
) -> float:
    """
    Calculates the enrichment factor at a given percentile.

    Args:
        df: DataFrame with docking results.
        active_column: Name of the column indicating active compounds.
        score_column: Name of the column with docking scores.
        percentile: The percentile at which to calculate the enrichment factor.

    Returns:
        The enrichment factor.
    """
    n_total = len(df)
    n_actives_total = df[active_column].sum()

    df_sorted = df.sort_values(score_column)
    top_percentile_df = df_sorted.head(int(n_total * percentile / 100))

    n_actives_top = top_percentile_df[active_column].sum()
    enrichment_factor = (n_actives_top / len(top_percentile_df)) / (
        n_actives_total / n_total
    )

    return enrichment_factor

def calculate_auc(df: pd.DataFrame, active_column: str, score_column: str) -> float:
    """
    Calculates the Area Under the ROC Curve (AUC).

    Args:
        df: DataFrame with docking results.
        active_column: Name of the column indicating active compounds.
        score_column: Name of the column with docking scores.

    Returns:
        The AUC score.
    """
    y_true = df[active_column]
    y_scores = -df[score_column]  # Negate scores because lower is better
    return roc_auc_score(y_true, y_scores)
