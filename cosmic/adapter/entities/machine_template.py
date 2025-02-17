# pragma: no cover
from typing import TypedDict, List, NotRequired


class State(TypedDict):
    """Represents a state in a machine template.
    It has a name and optional lists of `on_enter` and `on_exit` actions.
    """
    name: str
    on_enter: NotRequired[List[str]]
    on_exit: NotRequired[List[str]]


class Transition(TypedDict):
    """Represents a transition in a machine template.
    The `trigger` key represents the transition name, while `source` and `dest`
    represent the source and destination states, respectively. Make sure that
    the values of these keys are valid state names.
    The keys `conditions`, `unless`, `after`, and `before` are optional lists
    of conditions that must be met for the transition to be triggered.
    """
    trigger: str
    source: str  # assure that it represents a state name
    dest: str  # assure that it represents a state name
    conditions: NotRequired[List[str]]
    unless: NotRequired[List[str]]
    after: NotRequired[List[str]]
    before: NotRequired[List[str]]


class MachineTemplate(TypedDict):
    """Represents a machine template.
    The `initial_state` key represents the initial state of the machine.
    The `states` key is a list of states in the machine. See `State` for more
    information. The `transitions` key is a list of transitions in the machine.
    See `Transition` for more information.
    """
    initial_state: str
    states: List[State]
    transitions: List[Transition]
    declared_functions: NotRequired[List[str]]
