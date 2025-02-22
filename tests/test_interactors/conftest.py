import socket
from collections.abc import Generator
from pathlib import Path
from tempfile import gettempdir

import pytest


@pytest.fixture(scope="session")
def lock_file_path() -> str:
    file_name = socket.gethostname()
    file_path = Path(gettempdir()) / file_name
    file_path.unlink(missing_ok=True)
    return str(file_path)


@pytest.yield_fixture
def lock_file(lock_file_path: str) -> Generator[None, None, None]:
    open(lock_file_path, "w")
    yield
    Path(lock_file_path).unlink(missing_ok=True)
