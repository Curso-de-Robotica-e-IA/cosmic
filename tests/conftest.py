import pytest
from pathlib import Path


@pytest.fixture
def xml_file() -> Path:
    """Fixture to return a valid xml file path.

    Returns:
        Path: The path to the xml file.
    """
    file_path = Path('tests\\mock_files\\hcl_teste.xml')
    assert file_path.exists() and file_path.is_file()
    return file_path
