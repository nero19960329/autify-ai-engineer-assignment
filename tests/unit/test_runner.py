import pytest

from src.runner import run_python_code


def test_run_python_code_success():
    code = """
def add(a, b):
    return a + b
"""
    test_code = """
def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
"""
    result = run_python_code(code, test_code)
    assert result["result"] == "success"


def test_run_python_code_failure():
    code = """
def add(a, b):
    return a - b  # Intentional bug
"""
    test_code = """
def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
"""
    result = run_python_code(code, test_code)
    assert result["result"] == "failure"
    assert "AssertionError" in result["message"]


def test_run_python_code_timeout():
    code = """
def infinite_loop():
    while True:
        pass
"""
    test_code = """
def test_infinite_loop():
    infinite_loop()
"""
    result = run_python_code(code, test_code, timeout_ms=1000)
    assert result["result"] == "failure"


def test_run_python_code_memory_limit():
    code = """
def memory_exhausted():
    a = [i for i in range(10**6)]
    b = [i for i in range(10**6)]
    c = [i for i in range(10**6)]
"""
    test_code = """
def test_memory_exhausted():
    memory_exhausted()
"""
    result = run_python_code(code, test_code, memory_limit_mb=50)
    assert result["result"] == "failure"
