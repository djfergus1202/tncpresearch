"""
Command-Line Interface Module
============================

Main CLI entry points for TNCP-ResearchImagery.
"""

import typer
from typing import Optional, List
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import print as rprint

from ..core import TNPlatform, DataLoader
from ..models import GermLayerAnalyzer
from ..config import Config
from ..utils import logger

# Initialize Typer app
app = typer.Typer(
    name="tncp",
    help="TNCP-ResearchImagery: Translational NeuroCancer Platform CLI",
    add_completion=True,
)

console = Console()


@app.command()
def analyze(
    input: Path = typer.Argument(..., help="Input file or directory"),
    output: Path = typer.Option("./results", "--output", "-o", help="Output directory"),
    mode: str = typer.Option("auto", "--mode", "-m", help="Analysis mode"),
    cancer_type: Optional[str] = typer.Option(None, "--cancer-type", "-c", help="Cancer type for analysis"),
    config: Optional[Path] = typer.Option(None, "--config", help="Configuration file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Analyze medical images, molecular structures, or genomic data.
    """
    if verbose:
        console.print("[bold green]TNCP-ResearchImagery Analysis[/bold green]")
        console.print(f"Input: {input}")
        console.print(f"Output: {output}")
        console.print(f"Mode: {mode}")
        
    # Initialize platform
    platform = TNPlatform(config_path=str(config) if config else None)
    
    # Load data
    console.print("Loading data...")
    loader = DataLoader()
    
    try:
        data = loader.load(input)
        console.print(f"[green]✓[/green] Data loaded successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to load data: {e}")
        raise typer.Exit(1)
        
    # Determine analysis mode
    if mode == "auto":
        # Auto-detect mode based on file type
        if input.suffix in ['.pdb', '.cif']:
            mode = "molecular"
        elif input.suffix in ['.dcm', '.nii', '.nii.gz']:
            mode = "imaging"
        elif cancer_type:
            mode = "germ_layer"
        else:
            mode = "ml"
            
    console.print(f"Running [bold]{mode}[/bold] analysis...")
    
    # Run analysis
    with console.status("Analyzing...", spinner="dots"):
        try:
            if mode == "germ_layer" and cancer_type:
                analyzer = GermLayerAnalyzer()
                results = analyzer.analyze_cancer_type(cancer_type)
            else:
                results = platform.run_analysis(mode, data)
                
            # Save results
            output.mkdir(parents=True, exist_ok=True)
            output_file = output / f"results_{mode}.json"
            platform.save_results(str(output_file))
            
            console.print(f"[green]✓[/green] Analysis complete!")
            console.print(f"Results saved to: {output_file}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Analysis failed: {e}")
            raise typer.Exit(1)


@app.command()
def server(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Server host"),
    port: int = typer.Option(8000, "--port", "-p", help="Server port"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload"),
):
    """
    Start the TNCP web server.
    """
    console.print("[bold green]Starting TNCP Server[/bold green]")
    console.print(f"Host: {host}:{port}")
    
    try:
        import uvicorn
        from ..api import create_app
        
        app = create_app()
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except ImportError:
        console.print("[red]Server dependencies not installed![/red]")
        console.print("Install with: pip install tncp-researchimagery[api]")
        raise typer.Exit(1)


@app.command()
def germ_layer(
    cancer_type: str = typer.Argument(..., help="Cancer type to analyze"),
    expression: Optional[Path] = typer.Option(None, "--expression", "-e", help="Expression data file"),
    mutations: Optional[Path] = typer.Option(None, "--mutations", "-m", help="Mutation data file"),
    output: Path = typer.Option("./germ_layer_results.json", "--output", "-o", help="Output file"),
):
    """
    Perform germ layer analysis for a specific cancer type.
    """
    console.print(f"[bold]Germ Layer Analysis for {cancer_type}[/bold]")
    
    # Initialize analyzer
    analyzer = GermLayerAnalyzer()
    
    # Load optional data
    expression_data = None
    mutation_data = None
    
    if expression:
        loader = DataLoader()
        expression_data = loader.load(expression)
        console.print(f"Loaded expression data: {expression}")
        
    if mutations:
        loader = DataLoader()
        mutation_data = loader.load(mutations)
        console.print(f"Loaded mutation data: {mutations}")
        
    # Run analysis
    with console.status("Analyzing...", spinner="dots"):
        results = analyzer.analyze_cancer_type(
            cancer_type,
            expression_data=expression_data,
            mutation_data=mutation_data
        )
        
    # Display results
    table = Table(title=f"Germ Layer Analysis: {cancer_type}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Cancer Type", results['cancer_type'])
    table.add_row("Germ Layer", results['germ_layer'])
    table.add_row("Developmental Origin", str(results['developmental_origin'].get('origin', 'Unknown')))
    
    if results['treatment_recommendations']:
        therapies = [r['therapy'] for r in results['treatment_recommendations']]
        table.add_row("Recommended Therapies", ", ".join(therapies))
        
    if results['biomarkers']:
        markers = results['biomarkers'].get('known', [])
        table.add_row("Key Biomarkers", ", ".join(markers))
        
    if results['prognosis']:
        table.add_row("Median Survival", f"{results['prognosis'].get('median_survival', 'N/A')} months")
        table.add_row("Response Rate", f"{results['prognosis'].get('response_rate', 0)*100:.1f}%")
        
    console.print(table)
    
    # Save results
    import json
    with open(output, 'w') as f:
        json.dump(results, f, indent=2, default=str)
        
    console.print(f"\n[green]Results saved to: {output}[/green]")


@app.command()
def compare_layers():
    """
    Compare characteristics across different germ layers.
    """
    console.print("[bold]Germ Layer Comparison[/bold]\n")
    
    analyzer = GermLayerAnalyzer()
    comparison = analyzer.compare_germ_layers()
    
    # Create comparison table
    table = Table(title="Germ Layer Characteristics")
    
    for col in comparison.columns:
        table.add_column(col.replace('_', ' ').title(), style="cyan")
        
    for _, row in comparison.iterrows():
        table.add_row(*[str(v) for v in row.values])
        
    console.print(table)


@app.command()
def info():
    """
    Display platform information and status.
    """
    import tncp_researchimagery as tncp
    
    console.print("[bold green]TNCP-ResearchImagery Platform[/bold green]\n")
    
    table = Table(show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Version", tncp.__version__)
    table.add_row("Author", tncp.__author__)
    table.add_row("Contact", tncp.__email__)
    
    import platform
    table.add_row("Python", platform.python_version())
    table.add_row("System", platform.system())
    table.add_row("Platform", platform.platform())
    
    # Check dependencies
    import importlib
    deps = ["numpy", "torch", "pandas", "sklearn", "matplotlib"]
    installed = []
    missing = []
    
    for dep in deps:
        try:
            mod = importlib.import_module(dep)
            version = getattr(mod, "__version__", "unknown")
            installed.append(f"{dep} ({version})")
        except ImportError:
            missing.append(dep)
            
    if installed:
        table.add_row("Installed", ", ".join(installed[:3]) + "...")
        
    if missing:
        table.add_row("Missing", ", ".join(missing))
        
    console.print(table)
    
    # Check GPU availability
    try:
        import torch
        if torch.cuda.is_available():
            console.print(f"\n[green]✓[/green] GPU Available: {torch.cuda.get_device_name(0)}")
        else:
            console.print("\n[yellow]![/yellow] No GPU detected")
    except:
        pass


@app.command()
def test(
    module: Optional[str] = typer.Argument(None, help="Specific module to test"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Run platform tests.
    """
    console.print("[bold]Running TNCP Tests[/bold]\n")
    
    import subprocess
    
    cmd = ["pytest"]
    if module:
        cmd.append(f"tests/test_{module}.py")
    if verbose:
        cmd.append("-v")
        
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        console.print("[green]✓[/green] All tests passed!")
    else:
        console.print("[red]✗[/red] Some tests failed")
        console.print(result.stdout)
        
    raise typer.Exit(result.returncode)


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()