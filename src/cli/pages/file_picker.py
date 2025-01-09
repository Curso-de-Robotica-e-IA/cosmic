from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DirectoryTree


class FilePicker(Widget):

    def compose(self) -> ComposeResult:
        yield DirectoryTree('./')
