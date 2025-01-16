from transitions import State
from transitions.extensions import GraphMachine


class Sector(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `Sector` class.
        """
        waiting_ticket = State(
            name='waiting_ticket',
        )
        generating_ticket_emergency = State(
            name='generating_ticket_emergency',
        )
        send_ticket = State(
            name='send_ticket',
        )
        generating_ticket_icu = State(
            name='generating_ticket_icu',
        )
        generating_ticket_pediatrics = State(
            name='generating_ticket_pediatrics',
        )
        regenerating_icu_ticket = State(
            name='regenerating_icu_ticket',
        )
        regenerating_emergency_ticket = State(
            name='regenerating_emergency_ticket',
        )
        regenerating_pediatrics_ticket = State(
            name='regenerating_pediatrics_ticket',
        )

        states = ['waiting_ticket', 'generating_ticket_emergency', 'send_ticket', 'generating_ticket_icu', 'generating_ticket_pediatrics', 'regenerating_icu_ticket', 'regenerating_emergency_ticket', 'regenerating_pediatrics_ticket']

        transitions = [
            {'trigger': 'regenerating_pediatrics_ticket_to_waiting_ticket', 'source': 'regenerating_pediatrics_ticket', 'dest': 'waiting_ticket'},
            {'trigger': 'send_ticket_to_regenerating_pediatrics_ticket', 'source': 'send_ticket', 'dest': 'regenerating_pediatrics_ticket'},
            {'trigger': 'regenerating_emergency_ticket_to_waiting_ticket', 'source': 'regenerating_emergency_ticket', 'dest': 'waiting_ticket'},
            {'trigger': 'send_ticket_to_regenerating_emergency_ticket', 'source': 'send_ticket', 'dest': 'regenerating_emergency_ticket'},
            {'trigger': 'regenerating_icu_ticket_to_waiting_ticket', 'source': 'regenerating_icu_ticket', 'dest': 'waiting_ticket'},
            {'trigger': 'send_ticket_to_regenerating_icu_ticket', 'source': 'send_ticket', 'dest': 'regenerating_icu_ticket'},
            {'trigger': 'send_ticket_to_waiting_ticket', 'source': 'send_ticket', 'dest': 'waiting_ticket'},
            {'trigger': 'generating_ticket_pediatrics_to_send_ticket', 'source': 'generating_ticket_pediatrics', 'dest': 'send_ticket'},
            {'trigger': 'generating_ticket_icu_to_send_ticket', 'source': 'generating_ticket_icu', 'dest': 'send_ticket'},
            {'trigger': 'waiting_ticket_to_generating_ticket_icu', 'source': 'waiting_ticket', 'dest': 'generating_ticket_icu'},
            {'trigger': 'waiting_ticket_to_generating_ticket_pediatrics', 'source': 'waiting_ticket', 'dest': 'generating_ticket_pediatrics'},
            {'trigger': 'generating_ticket_emergency_to_send_ticket', 'source': 'generating_ticket_emergency', 'dest': 'send_ticket'},
            {'trigger': 'waiting_ticket_to_generating_ticket_emergency', 'source': 'waiting_ticket', 'dest': 'generating_ticket_emergency'},
        ]

        super().__init__(
            model=model,
            states=states,
            transitions=transitions,
            initial=waiting_ticket,
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
