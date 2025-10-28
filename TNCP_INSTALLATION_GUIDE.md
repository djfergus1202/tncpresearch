# TNCP-ResearchImagery Package Installation Guide

## 📦 Package Contents

The `tncp_researchimagery.tar.gz` archive contains a complete Python package for the Translational NeuroCancer Platform - Research Imagery and Analysis Toolkit.

## 🚀 Installation Instructions

### 1. Extract the Package
```bash
tar -xzf tncp_researchimagery.tar.gz
cd tncp_researchimagery
```

### 2. Install the Package

#### Option A: Install in Development Mode (Recommended for development)
```bash
pip install -e .
```

#### Option B: Install Normally
```bash
pip install .
```

#### Option C: Install with All Features
```bash
pip install -e ".[dev,docs,visualization,cuda]"
```

### 3. Verify Installation
```bash
# Check if the CLI is working
tncp --help

# Check package info
tncp info

# Run tests
pytest tests/
```

## 📊 Quick Start Examples

### Command Line Usage

1. **Germ Layer Analysis**
```bash
# Analyze a specific cancer type
tncp germ-layer NSCLC -o results.json

# Compare all germ layers
tncp compare-layers
```

2. **Start the Web Server**
```bash
tncp server --port 8000
```

3. **Analyze Medical Images**
```bash
tncp analyze /path/to/image.dcm --mode imaging
```

### Python API Usage

```python
from tncp_researchimagery import GermLayerAnalyzer, TNPlatform, set_seed

# Set seed for reproducibility
set_seed(42)

# Initialize analyzer
analyzer = GermLayerAnalyzer()

# Analyze cancer type
results = analyzer.analyze_cancer_type('NSCLC')
print(results)

# Compare germ layers
comparison = analyzer.compare_germ_layers()
print(comparison)
```

## 🔬 Key Features

### 1. **Germ Layer Analysis Framework**
- Novel approach to cancer classification based on embryonic origins
- Treatment recommendation engine
- Resistance pattern analysis
- Biomarker identification

### 2. **Comprehensive Cancer Type Coverage**
- **Ectoderm-derived**: GBM, Melanoma, Neuroblastoma, SCLC
- **Mesoderm-derived**: AML, CML, ALL, Sarcomas, RCC
- **Endoderm-derived**: NSCLC, Pancreatic, Colorectal, HCC
- **Mixed origin**: Breast, Ovarian, Prostate, Bladder

### 3. **Machine Learning Models**
- Drug response prediction
- Tumor segmentation
- Protein interaction mapping
- Survival analysis

### 4. **Medical Imaging Tools**
- DICOM/NIfTI support
- 3D visualization
- AI-powered segmentation
- Multi-modal registration

### 5. **Molecular Analysis**
- PDB structure analysis
- Molecular docking integration
- MD trajectory processing
- Interaction mapping

## 📁 Package Structure

```
tncp_researchimagery/
├── src/tncp_researchimagery/
│   ├── __init__.py          # Main package initialization
│   ├── cli/                 # Command-line interfaces
│   │   └── main.py          # Main CLI entry point
│   ├── core/                # Core platform functionality
│   ├── config/              # Configuration management
│   ├── models/              # ML/DL models
│   │   └── GermLayerAnalyzer # Novel germ layer framework
│   ├── utils/               # Utility functions
│   └── resources/           # Configuration files
├── examples/
│   ├── germ_layer_analysis.py  # Example analysis script
│   └── config.yaml             # Example configuration
├── tests/
│   └── test_basic.py           # Basic unit tests
├── pyproject.toml              # Modern Python packaging
├── README.md                   # Documentation
└── LICENSE                     # MIT License
```

## 🧬 Research Applications

1. **Cancer Therapy Response Prediction**
   - Based on embryonic germ layer origins
   - Personalized treatment recommendations
   - Resistance mechanism identification

2. **Drug Discovery Pipeline**
   - Virtual screening
   - ADMET prediction
   - Lead optimization

3. **Precision Medicine**
   - Patient stratification
   - Biomarker discovery
   - Treatment response prediction

4. **Imaging Biomarkers**
   - Radiomics features
   - Texture analysis
   - Multi-parametric integration

## 📋 Requirements

### Minimum Requirements
- Python >= 3.9
- NumPy, Pandas, Scikit-learn
- PyTorch >= 2.0.0

### Optional Dependencies
- CUDA support for GPU acceleration
- Medical imaging: SimpleITK, nibabel, pydicom
- Molecular: BioPython, RDKit, MDAnalysis
- Visualization: Matplotlib, Plotly, Seaborn

## 🔧 Configuration

The platform uses Hydra for configuration management. Create a `config.yaml` file:

```yaml
project_name: my_cancer_research
model:
  architecture: resnet50
  learning_rate: 0.001
data:
  data_dir: ./data
  batch_size: 32
```

## 📊 Example Output

When analyzing NSCLC (Non-Small Cell Lung Cancer):

```
Cancer Type: NSCLC
Germ Layer: endoderm
Origin: Inner embryonic layer
Recommended Therapies: chemotherapy, targeted_therapy, antiangiogenic
Key Biomarkers: KRAS, EGFR, HER2
Median Survival: 18 months
Response Rate: 45.0%
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

2. **CUDA Not Available**: Install PyTorch with CUDA support
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

3. **Permission Denied**: Use `--user` flag or virtual environment
```bash
pip install --user tncp-researchimagery
```

## 📚 Documentation

Full documentation available in the package:
- API Reference: See docstrings in source code
- Examples: Check `examples/` directory
- Tests: Run `pytest tests/` for usage examples

## 🤝 Support

- GitHub Issues: Report bugs or request features
- Email: david.ferguson@tncp.org
- Documentation: See README.md in package

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Developed by David Ferguson, PharmD Candidate at Howard University College of Pharmacy

---

**Version**: 0.1.0  
**Status**: Beta  
**Last Updated**: October 28, 2025