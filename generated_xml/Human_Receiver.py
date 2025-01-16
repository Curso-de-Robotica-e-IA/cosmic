from transitions import State
from transitions.extensions import GraphMachine


class Human_Receiver(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `Human_Receiver` class.
        """
        idle = State(
            name='idle',
        )
        receiving_pediatrics = State(
            name='receiving_pediatrics',
        )
        complete = State(
            name='complete',
        )
        icu_waiting = State(
            name='icu_waiting',
        )
        receiving_emergency = State(
            name='receiving_emergency',
        )
        receiving_icu = State(
            name='receiving_icu',
        )
        emergency_waiting = State(
            name='emergency_waiting',
        )
        pediatrics_waiting = State(
            name='pediatrics_waiting',
        )

        states = ['idle', 'receiving_pediatrics', 'complete', 'icu_waiting', 'receiving_emergency', 'receiving_icu', 'emergency_waiting', 'pediatrics_waiting']

        transitions = [
            {'trigger': 'pediatrics_waiting_to_receiving_pediatrics', 'source': 'pediatrics_waiting', 'dest': 'receiving_pediatrics'},
            {'trigger': 'emergency_waiting_to_receiving_emergency', 'source': 'emergency_waiting', 'dest': 'receiving_emergency'},
            {'trigger': 'icu_waiting_to_receiving_icu', 'source': 'icu_waiting', 'dest': 'receiving_icu'},
            {'trigger': 'idle_to_pediatrics_waiting', 'source': 'idle', 'dest': 'pediatrics_waiting'},
            {'trigger': 'idle_to_emergency_waiting', 'source': 'idle', 'dest': 'emergency_waiting'},
            {'trigger': 'receiving_icu_to_complete', 'source': 'receiving_icu', 'dest': 'complete'},
            {'trigger': 'receiving_emergency_to_complete', 'source': 'receiving_emergency', 'dest': 'complete'},
            {'trigger': 'idle_to_icu_waiting', 'source': 'idle', 'dest': 'icu_waiting'},
            {'trigger': 'complete_to_idle', 'source': 'complete', 'dest': 'idle'},
            {'trigger': 'receiving_pediatrics_to_complete', 'source': 'receiving_pediatrics', 'dest': 'complete'},
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
