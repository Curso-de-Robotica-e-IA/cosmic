from transitions import State
from transitions.extensions import GraphMachine


class Robot_Assembler(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `Robot_Assembler` class.
        """
        idle = State(
            name='idle',
        )
        working = State(
            name='working',
        )
        complete = State(
            name='complete',
        )
        prepare_kit = State(
            name='prepare_kit',
        )
        finish_ticket = State(
            name='finish_ticket',
        )
        decision = State(
            name='decision',
        )
        disobey = State(
            name='disobey',
        )
        disobey_icu = State(
            name='disobey_icu',
        )
        disobey_emergency = State(
            name='disobey_emergency',
        )
        disobey_pediatrics = State(
            name='disobey_pediatrics',
        )

        states = ['idle', 'working', 'complete', 'prepare_kit', 'finish_ticket', 'decision', 'disobey', 'disobey_icu', 'disobey_emergency', 'disobey_pediatrics']

        transitions = [
            {'trigger': 'disobey_icu_to_idle', 'source': 'disobey_icu', 'dest': 'idle', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'disobey_emergency_to_idle', 'source': 'disobey_emergency', 'dest': 'idle', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'disobey_pediatrics_to_idle', 'source': 'disobey_pediatrics', 'dest': 'idle', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'disobey_to_disobey_pediatrics', 'source': 'disobey', 'dest': 'disobey_pediatrics', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'disobey_to_disobey_emergency', 'source': 'disobey', 'dest': 'disobey_emergency', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'disobey_to_disobey_icu', 'source': 'disobey', 'dest': 'disobey_icu', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'decision_to_None', 'source': 'decision', 'dest': None, 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'idle_to_decision', 'source': 'idle', 'dest': 'decision', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'None_to_disobey', 'source': None, 'dest': 'disobey', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'None_to_working', 'source': None, 'dest': 'working', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'working_to_prepare_kit', 'source': 'working', 'dest': 'prepare_kit', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'finish_ticket_to_idle', 'source': 'finish_ticket', 'dest': 'idle', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'finish_ticket_to_complete', 'source': 'finish_ticket', 'dest': 'complete', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'working_to_finish_ticket', 'source': 'working', 'dest': 'finish_ticket', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'prepare_kit_to_working', 'source': 'prepare_kit', 'dest': 'working', 'conditions': ['is_ticket_queue_empty']},
            {'trigger': 'complete_to_idle', 'source': 'complete', 'dest': 'idle', 'conditions': ['is_ticket_queue_empty']},
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
