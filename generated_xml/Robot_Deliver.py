from transitions import State
from transitions.extensions import GraphMachine


class Robot_Deliver(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `Robot_Deliver` class.
        """
        idle = State(
            name='idle',
        )
        generating_path = State(
            name='generating_path',
        )
        arrived_pediatrics = State(
            name='arrived_pediatrics',
        )
        loading_icu_kits = State(
            name='loading_icu_kits',
        )
        working = State(
            name='working',
        )
        loading_emergency_kits = State(
            name='loading_emergency_kits',
        )
        delivering_emergency = State(
            name='delivering_emergency',
        )
        loading_pediatrics_kits = State(
            name='loading_pediatrics_kits',
        )
        returned = State(
            name='returned',
        )
        arrived_emergency = State(
            name='arrived_emergency',
        )
        arrived_icu = State(
            name='arrived_icu',
        )
        delivering_icu = State(
            name='delivering_icu',
        )
        delivering_pediatrics = State(
            name='delivering_pediatrics',
        )
        icu_delivery_done = State(
            name='icu_delivery_done',
        )
        emergency_delivery_done = State(
            name='emergency_delivery_done',
        )
        pediatrics_delivery_done = State(
            name='pediatrics_delivery_done',
        )

        states = ['idle', 'generating_path', 'arrived_pediatrics', 'loading_icu_kits', 'working', 'loading_emergency_kits', 'delivering_emergency', 'loading_pediatrics_kits', 'returned', 'arrived_emergency', 'arrived_icu', 'delivering_icu', 'delivering_pediatrics', 'icu_delivery_done', 'emergency_delivery_done', 'pediatrics_delivery_done']

        transitions = [
            {'trigger': 'pediatrics_delivery_done_to_returned', 'source': 'pediatrics_delivery_done', 'dest': 'returned', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'arrived_pediatrics_to_pediatrics_delivery_done', 'source': 'arrived_pediatrics', 'dest': 'pediatrics_delivery_done', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'emergency_delivery_done_to_returned', 'source': 'emergency_delivery_done', 'dest': 'returned', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'arrived_emergency_to_emergency_delivery_done', 'source': 'arrived_emergency', 'dest': 'emergency_delivery_done', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'icu_delivery_done_to_returned', 'source': 'icu_delivery_done', 'dest': 'returned', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'arrived_icu_to_icu_delivery_done', 'source': 'arrived_icu', 'dest': 'icu_delivery_done', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'delivering_pediatrics_to_arrived_pediatrics', 'source': 'delivering_pediatrics', 'dest': 'arrived_pediatrics', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'delivering_icu_to_arrived_icu', 'source': 'delivering_icu', 'dest': 'arrived_icu', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'working_to_delivering_pediatrics', 'source': 'working', 'dest': 'delivering_pediatrics', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'working_to_delivering_icu', 'source': 'working', 'dest': 'delivering_icu', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'delivering_emergency_to_arrived_emergency', 'source': 'delivering_emergency', 'dest': 'arrived_emergency', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'returned_to_idle', 'source': 'returned', 'dest': 'idle', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'returned_to_generating_path', 'source': 'returned', 'dest': 'generating_path', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery'], 'unless': ['all_served']},
            {'trigger': 'loading_pediatrics_kits_to_working', 'source': 'loading_pediatrics_kits', 'dest': 'working', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'working_to_loading_pediatrics_kits', 'source': 'working', 'dest': 'loading_pediatrics_kits', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'loading_emergency_kits_to_working', 'source': 'loading_emergency_kits', 'dest': 'working', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'working_to_loading_emergency_kits', 'source': 'working', 'dest': 'loading_emergency_kits', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'working_to_delivering_emergency', 'source': 'working', 'dest': 'delivering_emergency', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'loading_icu_kits_to_working', 'source': 'loading_icu_kits', 'dest': 'working', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'working_to_loading_icu_kits', 'source': 'working', 'dest': 'loading_icu_kits', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'generating_path_to_working', 'source': 'generating_path', 'dest': 'working', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
            {'trigger': 'idle_to_generating_path', 'source': 'idle', 'dest': 'generating_path', 'conditions': ['all_served', 'fill_with_sector_kits', 'delivery']},
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
