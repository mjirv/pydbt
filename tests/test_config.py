from pydbt.config import ConnectionConfig
import pytest
import os
from pathlib import Path

def test_config_from_env(tmp_path):
    env_content = """
PYDBT_BACKEND=duckdb
DUCKDB_PATH=:memory:
"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    
    config = ConnectionConfig.from_env(env_file)
    assert config.backend == "duckdb"
    assert config.connection_params["path"] == ":memory:"

def test_invalid_backend_config(tmp_path):
    env_content = "PYDBT_BACKEND=invalid"
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    
    with pytest.raises(ValueError):
        ConnectionConfig.from_env(env_file)