from textual import log
from textual.app import ComposeResult
from textual.containers import (
    Container,
    Horizontal,
)
from textual.widgets import (
    Button,
    ContentSwitcher,
    DirectoryTree,
    LoadingIndicator,
    Markdown,
    Placeholder,
)
from cli.components.dropdown import Dropdown
from cli.components.filtered_directory_tree import FilteredDirectoryTree


MAIN_PAGE_MARKDOWN = """
# COSMIC
_Code Output for State Machine Interactive Creation_

## Process
1. Load XML file
2. Review structure
3. Generate code
4. Test code
"""


class Main(Container):

    DEFAULT_CSS = """
    #buttons {
        height: 3;
        width: auto;
    }

    ContentSwitcher {
        border: round $primary;
        width: 90%;
        height: 1fr;
    }
    """

    xml_options = ['UPPAAL', 'ASTAH']
    output_options = ['pytransitions', 'python-state-machine']

    pages = [
        'main_page',
        'load_xml',
        'review_structure',
        'generate_code',
        'test_code',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_xml = None

    def compose(self) -> ComposeResult:
        with Horizontal(id='buttons'):
            yield Button(
                label='Load XML',
                id='load_xml',
            )
            yield Button(
                label='Review Structure',
                id='review_structure',
            )
            yield Button(
                label='Generate Code',
                id='generate_code',
            )
            yield Button(
                label='Test Code',
                id='test_code',
            )
            yield Dropdown(
                button_label='XML Dialect',
                list_content=self.xml_options,
                key=1,
                id='xml_option',
            )
            yield Dropdown(
                button_label='Output Dialect',
                list_content=self.output_options,
                key=2,
                id='output_option',
            )

        with ContentSwitcher(initial='main_page'):
            yield Container(
                Markdown(MAIN_PAGE_MARKDOWN),
                LoadingIndicator(name='loading_indicator'),
                id='main_page',
            )
            yield FilteredDirectoryTree(id='load_xml', path='~')
            yield Placeholder('Review Structure', id='review_structure', variant='text')  # noqa
            yield Placeholder('Review Generated Code', id='generate_code', variant='text')  # noqa
            yield Placeholder('Test Code', id='test_code', variant='text')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in self.pages:
            self.query_one(ContentSwitcher).current = event.button.id

    def on_directory_tree_file_selected(
        self,
        event: DirectoryTree.FileSelected,
    ) -> None:
        self.selected_xml = event.path
        log(self.selected_xml)
