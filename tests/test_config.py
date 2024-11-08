from pydbt.config import ConnectionConfig
import pytest

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

def test_missing_backend_config(tmp_path):
    env_content = "SOME_OTHER_VAR=value"
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    
    with pytest.raises(ValueError, match="PYDBT_BACKEND must be set"):
        ConnectionConfig.from_env(env_file)

def test_invalid_backend_config(tmp_path):
    env_content = "PYDBT_BACKEND=invalid_backend"
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    
    with pytest.raises(ValueError, match="Invalid backend"):
        ConnectionConfig.from_env(env_file)