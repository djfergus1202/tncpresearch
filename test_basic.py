"""
Basic tests for TNCP-ResearchImagery
"""

import pytest
import numpy as np
import pandas as pd
from tncp_researchimagery import (
    GermLayerAnalyzer,
    TNPlatform,
    Config,
    DataLoader,
    set_seed
)


def test_germ_layer_analyzer_init():
    """Test GermLayerAnalyzer initialization."""
    analyzer = GermLayerAnalyzer()
    assert analyzer is not None
    assert hasattr(analyzer, 'GERM_LAYER_MAP')
    assert hasattr(analyzer, 'TREATMENT_PATTERNS')


def test_cancer_type_classification():
    """Test cancer type germ layer classification."""
    analyzer = GermLayerAnalyzer()
    
    # Test known cancer types
    assert analyzer.GERM_LAYER_MAP['GBM'] == 'ectoderm'
    assert analyzer.GERM_LAYER_MAP['NSCLC'] == 'endoderm'
    assert analyzer.GERM_LAYER_MAP['AML'] == 'mesoderm'
    
    # Test analysis
    result = analyzer.analyze_cancer_type('GBM')
    assert result['cancer_type'] == 'GBM'
    assert result['germ_layer'] == 'ectoderm'


def test_treatment_recommendations():
    """Test treatment recommendation generation."""
    analyzer = GermLayerAnalyzer()
    
    result = analyzer.analyze_cancer_type('NSCLC')
    assert 'treatment_recommendations' in result
    assert len(result['treatment_recommendations']) > 0
    
    # Check structure
    rec = result['treatment_recommendations'][0]
    assert 'therapy' in rec
    assert 'rationale' in rec
    assert 'priority' in rec


def test_platform_initialization():
    """Test TNPlatform initialization."""
    platform = TNPlatform()
    assert platform is not None
    assert hasattr(platform, 'config')
    assert hasattr(platform, 'pipelines')


def test_config_management():
    """Test configuration management."""
    config = Config()
    assert config is not None
    
    # Test getting values
    assert config.get('version') is not None
    
    # Test setting values
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'


def test_data_loader():
    """Test DataLoader functionality."""
    loader = DataLoader()
    assert loader is not None
    
    # Test loading different formats (would need actual files in real tests)
    # This is a placeholder for actual file loading tests


def test_seed_setting():
    """Test reproducibility with seed setting."""
    set_seed(42)
    
    # Generate random numbers
    np_random1 = np.random.random(10)
    
    # Reset seed and generate again
    set_seed(42)
    np_random2 = np.random.random(10)
    
    # Should be identical
    assert np.allclose(np_random1, np_random2)


def test_germ_layer_comparison():
    """Test germ layer comparison functionality."""
    analyzer = GermLayerAnalyzer()
    comparison = analyzer.compare_germ_layers()
    
    assert isinstance(comparison, pd.DataFrame)
    assert 'germ_layer' in comparison.columns
    assert len(comparison) == 3  # ectoderm, mesoderm, endoderm


def test_with_expression_data():
    """Test analysis with expression data."""
    analyzer = GermLayerAnalyzer()
    
    # Create synthetic expression data
    expression_data = pd.DataFrame(
        np.random.randn(100, 20),
        columns=[f"Gene_{i}" for i in range(20)]
    )
    
    result = analyzer.analyze_cancer_type(
        'NSCLC',
        expression_data=expression_data
    )
    
    assert 'expression_analysis' in result
    assert result['expression_analysis']['num_genes'] == 20


def test_with_mutation_data():
    """Test analysis with mutation data."""
    analyzer = GermLayerAnalyzer()
    
    # Create synthetic mutation data
    mutation_data = pd.DataFrame({
        'gene': ['TP53', 'KRAS', 'EGFR'],
        'mutation_type': ['missense', 'missense', 'deletion'],
        'frequency': [0.5, 0.3, 0.2]
    })
    
    result = analyzer.analyze_cancer_type(
        'NSCLC',
        mutation_data=mutation_data
    )
    
    assert 'mutation_analysis' in result
    assert result['mutation_analysis']['mutation_burden'] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])