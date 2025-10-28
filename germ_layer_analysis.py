#!/usr/bin/env python
"""
Example: Germ Layer Analysis for Cancer Research

This example demonstrates how to use TNCP-ResearchImagery to analyze
cancer types based on their embryonic germ layer origins.

Author: David Ferguson
"""

import pandas as pd
import numpy as np
from tncp_researchimagery import (
    GermLayerAnalyzer,
    TNPlatform,
    Config,
    set_seed
)

def main():
    """Run example germ layer analysis."""
    
    # Set seed for reproducibility
    set_seed(42)
    
    print("=" * 60)
    print("TNCP-ResearchImagery: Germ Layer Analysis Example")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = GermLayerAnalyzer()
    
    # Define cancer types to analyze
    cancer_types = [
        'GBM',      # Glioblastoma (Ectoderm)
        'NSCLC',    # Non-small cell lung cancer (Endoderm)
        'AML',      # Acute myeloid leukemia (Mesoderm)
        'PANCREATIC',  # Pancreatic cancer (Endoderm)
        'MELANOMA',    # Melanoma (Ectoderm)
    ]
    
    print("\n📊 Analyzing Cancer Types by Germ Layer Origin\n")
    
    # Analyze each cancer type
    results = {}
    for cancer_type in cancer_types:
        print(f"Analyzing {cancer_type}...")
        
        # Generate synthetic expression data for demonstration
        expression_data = pd.DataFrame(
            np.random.randn(100, 20),
            columns=[f"Gene_{i}" for i in range(20)]
        )
        
        # Generate synthetic mutation data
        mutation_data = pd.DataFrame({
            'gene': ['TP53', 'KRAS', 'EGFR', 'BRAF', 'PIK3CA'],
            'mutation_type': ['missense', 'missense', 'deletion', 'missense', 'amplification'],
            'frequency': np.random.random(5)
        })
        
        # Run analysis
        analysis = analyzer.analyze_cancer_type(
            cancer_type,
            expression_data=expression_data,
            mutation_data=mutation_data
        )
        
        results[cancer_type] = analysis
        
        # Display key findings
        print(f"  ├─ Germ Layer: {analysis['germ_layer']}")
        print(f"  ├─ Origin: {analysis['developmental_origin'].get('origin', 'Unknown')}")
        
        if analysis['treatment_recommendations']:
            therapies = [r['therapy'] for r in analysis['treatment_recommendations'][:3]]
            print(f"  ├─ Recommended: {', '.join(therapies)}")
            
        print(f"  └─ Prognosis: {analysis['prognosis'].get('median_survival', 'N/A')} months\n")
    
    # Compare germ layers
    print("\n📈 Germ Layer Comparison\n")
    comparison = analyzer.compare_germ_layers()
    print(comparison.to_string())
    
    # Summary statistics
    print("\n📊 Summary Statistics\n")
    
    germ_layer_counts = {}
    for cancer_type, result in results.items():
        layer = result['germ_layer']
        germ_layer_counts[layer] = germ_layer_counts.get(layer, 0) + 1
    
    for layer, count in germ_layer_counts.items():
        print(f"  {layer.capitalize()}: {count} cancer type(s)")
    
    # Treatment pattern analysis
    print("\n💊 Treatment Patterns by Germ Layer\n")
    
    treatment_summary = {}
    for layer in ['ectoderm', 'mesoderm', 'endoderm']:
        patterns = analyzer.TREATMENT_PATTERNS[layer]
        treatment_summary[layer] = {
            'therapies': patterns['preferred_therapies'],
            'resistance': patterns['resistance_mechanisms'],
            'biomarkers': patterns['biomarkers']
        }
        
        print(f"  {layer.capitalize()}:")
        print(f"    Therapies: {', '.join(patterns['preferred_therapies'])}")
        print(f"    Resistance: {', '.join(patterns['resistance_mechanisms'])}")
        print(f"    Biomarkers: {', '.join(patterns['biomarkers'])}\n")
    
    # Platform integration example
    print("\n🔧 Platform Integration Example\n")
    
    # Initialize platform
    config = Config()
    platform = TNPlatform(config_path=None)
    
    # Get platform summary
    summary = platform.get_summary()
    print(f"Platform Version: {summary['platform_version']}")
    print(f"Available Pipelines: {', '.join(summary['pipelines'])}")
    
    print("\n✅ Analysis Complete!")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    results = main()