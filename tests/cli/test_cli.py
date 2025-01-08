import pytest
from src.cli.cli import CommandLineInterface
from rich import terminal_theme


@pytest.mark.parametrize(
    'theme, expected',
    [
        ('default', terminal_theme.DEFAULT_TERMINAL_THEME),
        ('monokai', terminal_theme.MONOKAI),
        ('dimmed_monokai', terminal_theme.DIMMED_MONOKAI),
        ('night_owlish', terminal_theme.NIGHT_OWLISH),
        ('invalid', terminal_theme.DEFAULT_TERMINAL_THEME),
    ]
)
def test_cli_parse_theme(theme, expected):
    assert CommandLineInterface._parse_theme(theme) == expected
