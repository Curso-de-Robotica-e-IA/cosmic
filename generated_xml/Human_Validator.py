from transitions import State
from transitions.extensions import GraphMachine


class Human_Validator(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `Human_Validator` class.
        """
        idle = State(
            name='idle',
        )
        validating = State(
            name='validating',
        )
        complete = State(
            name='complete',
        )

        states = ['idle', 'validating', 'complete']

        transitions = [
            {'trigger': 'complete_to_idle', 'source': 'complete', 'dest': 'idle'},
            {'trigger': 'idle_to_validating', 'source': 'idle', 'dest': 'validating'},
            {'trigger': 'validating_to_complete', 'source': 'validating', 'dest': 'complete'},
        ]

        super().__init__(
            model=model,
            states=states,
            transitions=transitions,
            initial=idle,
        )

    def __getattr__(self, item):
        """Method to get unlisted attributes of the class. If the attribute
        is not found, the method will return the class attribute.

        Args:
            item: The class attribute that should be retrieved.

        Returns:
            The class attribute.
        """
        self.model.__getattribute__(item)

    def next_state(self):
        """Method for automatic execution of available transitions in each
        of the machine states.
        """
        available_transitions = self.get_triggers(self.state)
        available_transitions = available_transitions[len(self.states):]

        LOGGER.debug(f'Available transitions: {available_transitions}')

        for curr_transition in available_transitions:
            may_method_result = self.may_trigger(curr_transition)
            if may_method_result:
                LOGGER.debug(f'Transition executed: {curr_transition}')
                self.trigger(curr_transition)
