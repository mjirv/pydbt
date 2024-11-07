import pytest
import ibis
import pandas as pd
from pathlib import Path

@pytest.fixture
def mock_connection():
    return ibis.duckdb.connect(":memory:")

@pytest.fixture
def sample_model_path(tmp_path):
    model_path = tmp_path / "sample_model.py"
    model_path.write_text("""
def run(con, ibis):
    return con.table('test').filter(col1 > 0)
""")
    return model_path