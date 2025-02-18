<%!
from mako.template import Template
%>\
from transitions import State
from transitions.extensions import GraphMachine


class ${agent_name}(GraphMachine):

    def __init__(self, model) -> None:
        """Constructor of the base `${agent_name}` class.
        """
        % for state in states:
        ${state['name']} = State(
            name='${state['name']}',
            % if state.get('on_enter', None) is not None:
            on_enter=${state['on_enter']},
            % endif
            %if state.get('on_exit', None) is not None:
            on_exit=${state['on_exit']},
            % endif
        )
        % endfor

        states = [
            % for state in states:
            ${state['name']},
            % endfor
        ]

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
        return self.model.__getattribute__(item)

    def next_state(self):
        """Method for automatic execution of available transitions in each
        of the machine states.
        """
        available_transitions = self.get_triggers(self.state)
        available_transitions = available_transitions[len(self.states):]

        for curr_transition in available_transitions:
            may_method_result = self.may_trigger(curr_transition)
            if may_method_result:
                self.trigger(curr_transition)
