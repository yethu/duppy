import subprocess
import sys
import os


def run_cli(args):
    script = os.path.abspath("main.py")
    return subprocess.run(
        [sys.executable, script] + args, capture_output=True, text=True
    )


def test_chunk_size_invalid_zero():
    result = run_cli([".", "--chunk-size", "0"])
    assert result.returncode != 0
    assert "0 is an invalid chunk size value" in result.stderr


def test_chunk_size_invalid_negative():
    result = run_cli([".", "--chunk-size", "-100"])
    assert result.returncode != 0
    assert "-100 is an invalid chunk size value" in result.stderr


def test_chunk_size_invalid_string():
    result = run_cli([".", "--chunk-size", "notanumber"])
    assert result.returncode != 0
    assert "invalid validate_positive value" in result.stderr


def test_chunk_size_valid():
    result = run_cli([".", "--chunk-size", "4096"])
    assert (
        "Duplicate files found:" in result.stdout
        or "No duplicate files found." in result.stdout
    )
