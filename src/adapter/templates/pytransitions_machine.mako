<%!
from mako.template import Template
%>
from transitions import State
from transitions.extensions import GraphMachine


class ${agent_name}(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `${agent_name}` class.
        """
        % for state in states:
        ${state} = State(
            name='${state}',
        )
        % endfor

        states = ${states}

        transitions = [
            % for transition in transitions:
            ${transition},
            % endfor 
        ]

        super().__init__(
            model=model,
            states=states,
            transitions=transitions,
            initial=${initial_state},
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