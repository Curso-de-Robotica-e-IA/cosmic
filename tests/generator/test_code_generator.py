import pytest
from pathlib import Path
from cosmic.generator.code_generator import CodeGenerator
from unittest.mock import MagicMock


@pytest.fixture
def code_generator():
    return CodeGenerator(
        'uppaal',
        'pytransitions',
    )


@pytest.fixture
def xml_file():
    file_path = Path('tests\\mock_files\\hcl_teste.xml')
    assert file_path.exists() and file_path.is_file()
    return file_path


@pytest.fixture
def result_dict_mock():
    return {
        'MockMachine': {
            'states': ['A', 'B', 'C'],
            'transitions': [
                {
                    'name': 't1',
                    'source': 'A',
                    'dest': 'B',
                    'conditions': ['is_valid'],
                },
                {
                    'name': 't2',
                    'source': 'B',
                    'dest': 'C',
                },
            ],
            'initial_state': 'A',
        }
    }


def test_get_template_file_returns_a_valid_file():
    template_file = CodeGenerator.get_template_file(
        'pytransitions',
    )
    assert template_file.exists() and template_file.is_file()


def test_get_template_file_raises_not_implemented_error():
    with pytest.raises(NotImplementedError):
        CodeGenerator.get_template_file('other_dialect')


def test_generate_code_raises_file_not_found_error(code_generator):
    with pytest.raises(FileNotFoundError):
        code_generator.generate_code(
            'invalid.xml',
            Path('tests/generator/tmp'),
        )


def test_generated_code_is_saved_in_output_dir(
    code_generator,
    xml_file,
    result_dict_mock,
    tmp_path,
):
    output_path = tmp_path / 'output'
    output_path.mkdir()

    mock_adapter = MagicMock()
    mock_adapter.parse_xml.return_value = 'mocked_root'
    mock_adapter.get_xml_data.return_value = result_dict_mock

    code_generator.xml_adapter = mock_adapter

    code_generator.generate_code(
        xml_file=xml_file,
        output_dir=output_path,
    )

    assert len(list(output_path.iterdir())) == 1
