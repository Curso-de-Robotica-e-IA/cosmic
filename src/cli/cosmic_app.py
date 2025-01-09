from cli.pages.main import Main
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class Cosmic(App):

    CSS_PATH = 'css/cosmic.tcss'
    BINDINGS = [
        ('r', 'rerun', 'Rerun'),
        ('d', 'toggle_dark', 'Toggle Dark Mode'),
    ]

    menu_options = {
        'load_xml': lambda: print('load_xml'),
        'review_structure': lambda: print('review_structure'),
        'generate_code': lambda: print('generate_code'),
        'test_code': lambda: print('test_code'),
        'exit': lambda: print('exit'),
    }

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True,
            time_format='%H:%M:%S',
            name='header',
        )
        yield Footer()
        yield Main()

    def action_rerun(self):
        """An action to rerun the app."""
        print('Rerunning...')

    def action_toggle_dark(self):
        """An action to toggle dark mode."""
        if self.theme == 'textual-light':
            self.theme = 'textual-dark'
        else:
            self.theme = 'textual-light'
