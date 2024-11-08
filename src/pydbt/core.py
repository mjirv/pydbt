from pathlib import Path
from typing import Callable, Any
import ibis
import importlib.util
from .config import ConnectionConfig

def get_ibis_connection(config: ConnectionConfig) -> Any:
    """Creates an Ibis connection based on the configuration."""
    if config.backend == "duckdb":
        return ibis.duckdb.connect(**config.connection_params)
    elif config.backend == "postgres":
        return ibis.postgres.connect(**config.connection_params)
    elif config.backend == "bigquery":
        return ibis.bigquery.connect(**config.connection_params)
    elif config.backend == "snowflake":
        return ibis.snowflake.connect(**config.connection_params)
    else:
        raise ValueError(f"Unsupported backend: {config.backend}")

def load_python_model(path: Path) -> Callable:
    """Loads a Python model file and returns its run function."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load {path}")
        
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if not hasattr(module, "run"):
        raise AttributeError(f"Model {path} must define a run function")
    
    return module.run

def run_all_models(pydbt_dir: Path, models_dir: Path, config: ConnectionConfig) -> None:
    """Runs all Python models and generates corresponding SQL files."""
    con = get_ibis_connection(config)
    
    # Iterate over all Python files in the pydbt directory except tests
    for py_path in pydbt_dir.rglob("*.py"):
        if py_path.name == "__init__.py" or py_path.name.endswith("_test.py"):
            continue
            
        relative_path = py_path.relative_to(pydbt_dir)
        sql_path = models_dir / relative_path.with_suffix(".sql")
        
        # Create parent directories if they don't exist
        sql_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load and run the model
        run_func = load_python_model(py_path)
        projection = run_func(con, ibis)
        
        # Generate and save SQL
        sql = projection.compile()
        sql_path.write_text(sql)
