from textual.containers import (
    Container,
    HorizontalGroup,
    VerticalGroup,
    VerticalScroll,
)
from textual.widgets import (
    Button,
)


class Main(Container):

    def compose(self):
        yield HorizontalGroup(
            VerticalGroup(
                Button(label='Load XML', id='load_xml'),
                Button(label='Review Structure', id='review_structure'),
                Button(label='Generate Code', id='generate_code'),
                Button(label='Test Code', id='test_code'),
            ),

            VerticalScroll(),
        )
