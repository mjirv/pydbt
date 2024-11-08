# src/pydbt/cli.py
import click
from pathlib import Path
import shutil
from typing import Optional
from .core import run_all_models
from .config import ConnectionConfig
from .testing import ModelTester

@click.group()
def cli():
    """PyDBT - Python-based DBT helper using Ibis"""
    pass

@cli.command()
def init():
    """Initialize a new PyDBT project"""
    pydbt_dir = Path("pydbt")
    pydbt_dir.mkdir(exist_ok=True)
    
    # Copy example model
    example_path = Path(__file__).parent / "templates" / "your_first_model.py"
    shutil.copy(example_path, pydbt_dir / "your_first_model.py")

    test_path = Path(__file__).parent / "templates" / "your_first_model_test.py"
    shutil.copy(test_path, pydbt_dir / "your_first_model_test.py")
    
    # Create .env.example
    env_example = """
# Choose your backend: duckdb, postgres, bigquery, or snowflake
PYDBT_BACKEND=duckdb

# DuckDB
DUCKDB_DATABASE=:memory:

# PostgreSQL
#PG_HOST=localhost
#PG_PORT=5432
#PG_USER=postgres
#PG_PASSWORD=postgres
#PG_DATABASE=database

# BigQuery
#BQ_PROJECT=your-project-id
#BQ_CREDENTIALS=/path/to/credentials.json

# Snowflake
#SF_ACCOUNT=your-account
#SF_USER=your-user
#SF_PASSWORD=your-password
#SF_DATABASE=your-database
#SF_WAREHOUSE=your-warehouse
    """.strip()
    
    (pydbt_dir / ".env.example").write_text(env_example)
    click.echo("Created .env.example - copy to .env and configure your connection")
    
    # Create .gitignore
    gitignore = """
.env
__pycache__/
*.pyc
    """.strip()
    
    (pydbt_dir / ".gitignore").write_text(gitignore)
    click.echo("Initialized PyDBT project in ./pydbt")

@cli.command()
def run():
    """Run all Python models and generate SQL"""
    pydbt_dir = Path("pydbt")
    models_dir = Path("models")
    
    if not pydbt_dir.exists():
        raise click.ClickException("No pydbt directory found. Run 'pydbt init' first.")
    
    if not models_dir.exists():
        raise click.ClickException("No models directory found. Is this a DBT project?")
    
    config = ConnectionConfig.from_env(pydbt_dir / ".env")
    run_all_models(pydbt_dir, models_dir, config)
    click.echo("Generated SQL files for all models")

@cli.command()
@click.option('--model', help='Specific model to test (defaults to all)')
def test(model: Optional[str]):
    """Run tests for PyDBT models"""
    pydbt_dir = Path("pydbt")
    
    if not pydbt_dir.exists():
        raise click.ClickException("No pydbt directory found. Run 'pydbt init' first.")
    
    failed_tests = 0
    total_tests = 0
    
    def run_model_tests(model_path: Path) -> None:
        nonlocal failed_tests, total_tests
        
        test_path = model_path.parent / f"{model_path.stem}_test.py" 
        if not test_path.exists():
            click.echo(f"No tests found for {model_path.name}")
            return
            
        click.echo(f"\nRunning tests for {model_path.name}:")
        tester = ModelTester(model_path, test_path)
        results = tester.run_tests()
        
        for result in results:
            total_tests += 1
            status = "✓" if result["success"] else "✗"
            if not result["success"]:
                failed_tests += 1
            click.echo(f"{status} {result['name']}: {result['message']}")
    
    if model:
        model_path = pydbt_dir / f"{model}.py"
        if not model_path.exists():
            raise click.ClickException(f"Model {model} not found")
        run_model_tests(model_path)
    else:
        for model_path in pydbt_dir.rglob("*.py"):
            if model_path.name.endswith("_test.py") or model_path.name == "__init__.py":
                continue
            run_model_tests(model_path)
    
    click.echo(f"\nTest Results: {total_tests - failed_tests}/{total_tests} passed")
    if failed_tests > 0:
        raise click.ClickException(f"{failed_tests} test(s) failed")