from rich import terminal_theme
from rich.console import Console
from typing import Literal


THEMES = Literal['default', 'monokai', 'dimmed_monokai', 'night_owlish']


class CommandLineInterface:

    @staticmethod
    def _parse_theme(theme: THEMES) -> terminal_theme.TerminalTheme:
        values = {
            "default": terminal_theme.DEFAULT_TERMINAL_THEME,
            "monokai": terminal_theme.MONOKAI,
            "dimmed_monokai": terminal_theme.DIMMED_MONOKAI,
            "night_owlish": terminal_theme.NIGHT_OWLISH,
        }
        if theme not in values.keys():
            return values['default']
        return values[theme]

    def __init__(
        self,
        theme: THEMES = 'default',
    ):
        self.console = Console(
            theme=self._parse_theme(theme)
        )
