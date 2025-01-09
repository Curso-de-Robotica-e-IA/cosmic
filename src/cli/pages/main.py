from textual.containers import (
    Container,
    HorizontalGroup,
    VerticalGroup,
)
from textual.widgets import (
    Button,
    Placeholder,
    ContentSwitcher,
)
from cli.components.dropdown import Dropdown


class Main(Container):

    xml_options = ['UPPAAL', 'ASTAH']
    output_options = ['pytransitions', 'python-state-machine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable_review_structure = False
        self.enable_generate_code = False
        self.enable_test_code = False
        self.screen_content = None

    def compose(self):
        yield VerticalGroup(
            HorizontalGroup(
                Button(label='Load XML', id='load_xml'),
                Dropdown(
                    button_label='XML Dialect',
                    list_content=self.xml_options,
                    key=1,
                    id='xml_option',
                ),
                Dropdown(
                    button_label='Output Dialect',
                    list_content=self.output_options,
                    key=2,
                    id='output_option',
                ),
                Button(
                    label='Review Structure',
                    id='review_structure',
                ),
                Button(
                    label='Generate Code',
                    id='generate_code',
                ),
                Button(
                    label='Test Code',
                    id='test_code',
                ),
            ),
            Placeholder(),
        )
