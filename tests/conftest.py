import pytest


def pytest_runtest_logstart(nodeid, location):
    # Emit a simple marker when each test begins
    print(f"[TEST START] {nodeid}")


def pytest_runtest_logfinish(nodeid, location):
    # Emit a marker when each test completes
    print(f"[TEST END] {nodeid}")