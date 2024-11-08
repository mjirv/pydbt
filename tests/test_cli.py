from pathlib import Path
from click.testing import CliRunner
from pydbt.cli import cli
import pytest

def test_init_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert (Path("pydbt") / "your_first_model.py").exists()
        assert (Path("pydbt") / ".env.example").exists()

def test_run_command_no_pydbt_dir():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["run"])
        assert result.exit_code != 0
        assert "No pydbt directory found" in result.output

def test_test_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # First init the project
        runner.invoke(cli, ["init"])
        # Then run tests
        result = runner.invoke(cli, ["test"])
        assert result.exit_code == 0