from textual import log
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Button, OptionList


class Dropdown(HorizontalGroup):

    DEFAULT_CSS = """
    Dropdown {
        width: auto;
        height: auto;
        layout: horizontal;
        overflow: hidden hidden;
    }

    .hidden {
        display: none;
    }
    """

    def __init__(
        self,
        button_label: str,
        list_content: list[str],
        key: int = 0,
        *args,
        **kwargs,
    ) -> None:
        self.list_content = list_content
        self.button_label = button_label
        self.key = key
        self.button_id = f'dropdown_button_{self.key}'
        self.option_list_id = f'dropdown_option_{self.key}'
        self.button = Button(
            label=f'{self.button_label} ↓',
            id=self.button_id,
        )
        self.option_list = OptionList(
            *self.list_content,
            id=self.option_list_id,
            tooltip=f'Select the {self.button_label}',
            classes='hidden',
        )
        self.choice = list_content[0]
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        log(locals())
        log(self.tree)
        yield self.button
        yield self.option_list

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        log(event)
        self.button.add_class('hidden')
        self.option_list.remove_class('hidden')

    def on_option_list_option_selected(
        self,
        event: OptionList.OptionSelected,
    ) -> None:
        """Event handler called when an option is selected."""
        log(event)
        self.choice = self.list_content[event.option_index]
        log(self.choice)
        self.option_list.add_class('hidden')
        self.button.remove_class('hidden')
