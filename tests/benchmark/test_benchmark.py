
import pandas as pd
import pytest

from naturaDock.benchmark import calculate_enrichment_factor, calculate_auc

@pytest.fixture
def sample_benchmark_data():
    """Provides a sample DataFrame for benchmark tests."""
    data = {
        'compound_id': [f'comp_{i}' for i in range(20)],
        'is_active': [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'vina_score': [-10.5, -9.8, -9.5, -8.2, -8.1, -7.5, -7.4, -7.3, -7.2, -7.1, -7.0, -6.9, -6.8, -6.7, -6.6, -6.5, -6.4, -6.3, -6.2, -6.1]
    }
    return pd.DataFrame(data)

def test_calculate_enrichment_factor(sample_benchmark_data):
    """Tests the calculate_enrichment_factor function."""
    ef = calculate_enrichment_factor(sample_benchmark_data, 'is_active', 'vina_score', 10)
    assert isinstance(ef, float)
    assert ef > 1.0

def test_calculate_auc(sample_benchmark_data):
    """Tests the calculate_auc function."""
    auc = calculate_auc(sample_benchmark_data, 'is_active', 'vina_score')
    assert isinstance(auc, float)
    assert 0.5 <= auc <= 1.0
