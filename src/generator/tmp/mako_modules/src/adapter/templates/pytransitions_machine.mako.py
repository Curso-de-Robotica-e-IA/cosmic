# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1736788140.5880535
_enable_loop = True
_template_filename = 'src/adapter/templates/pytransitions_machine.mako'
_template_uri = 'src/adapter/templates/pytransitions_machine.mako'
_source_encoding = 'utf-8'
_exports = []



from mako.template import Template


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        states = context.get('states', UNDEFINED)
        transitions = context.get('transitions', UNDEFINED)
        initial_state = context.get('initial_state', UNDEFINED)
        agent_name = context.get('agent_name', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('from transitions import State\nfrom transitions.extensions import GraphMachine\n\n\nclass ')
        __M_writer(str(agent_name))
        __M_writer('(GraphMachine):\n\n    def __init__(self, model) -> None:\n        """Constructor of the base `')
        __M_writer(str(agent_name))
        __M_writer('` class.\n        """\n')
        for state in states:
            __M_writer('        ')
            __M_writer(str(state))
            __M_writer(" = State(\n            name='")
            __M_writer(str(state))
            __M_writer("',\n        )\n")
        __M_writer('\n        states = ')
        __M_writer(str(states))
        __M_writer('\n\n        transitions = [\n')
        for transition in transitions:
            __M_writer('            ')
            __M_writer(str(transition))
            __M_writer(',\n')
        __M_writer('        ]\n\n        super().__init__(\n            model=model,\n            states=states,\n            transitions=transitions,\n            initial=')
        __M_writer(str(initial_state))
        __M_writer(',\n        )\n\n    def __getattr__(self, item):\n        """Method to get unlisted attributes of the class. If the attribute\n        is not found, the method will return the class attribute.\n\n        Args:\n            item: The class attribute that should be retrieved.\n\n        Returns:\n            The class attribute.\n        """\n        self.model.__getattribute__(item)\n\n    def next_state(self):\n        """Method for automatic execution of available transitions in each\n        of the machine states.\n        """\n        available_transitions = self.get_triggers(self.state)\n        available_transitions = available_transitions[len(self.states):]\n\n        LOGGER.debug(f\'Available transitions: {available_transitions}\')\n\n        for curr_transition in available_transitions:\n            may_method_result = self.may_trigger(curr_transition)\n            if may_method_result:\n                LOGGER.debug(f\'Transition executed: {curr_transition}\')\n                self.trigger(curr_transition)\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "src/adapter/templates/pytransitions_machine.mako", "uri": "src/adapter/templates/pytransitions_machine.mako", "source_encoding": "utf-8", "line_map": {"16": 1, "17": 2, "18": 3, "19": 4, "20": 0, "29": 4, "30": 8, "31": 8, "32": 11, "33": 11, "34": 13, "35": 14, "36": 14, "37": 14, "38": 15, "39": 15, "40": 18, "41": 19, "42": 19, "43": 22, "44": 23, "45": 23, "46": 23, "47": 25, "48": 31, "49": 31, "55": 49}}
__M_END_METADATA
"""
