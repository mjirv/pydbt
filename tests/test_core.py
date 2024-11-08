import pytest
from pydbt.core import load_python_model, get_ibis_connection
from pydbt.config import ConnectionConfig
import pandas as pd

def test_load_python_model(sample_model_path):
    run_func = load_python_model(sample_model_path)
    assert callable(run_func)

def test_get_ibis_connection():
    config = ConnectionConfig(
        backend="duckdb",
        connection_params={"database": ":memory:"}
    )
    con = get_ibis_connection(config)
    assert con is not None

def test_invalid_backend():
    config = ConnectionConfig(
        backend="invalid",
        connection_params={}
    )
    with pytest.raises(ValueError):
        get_ibis_connection(config)