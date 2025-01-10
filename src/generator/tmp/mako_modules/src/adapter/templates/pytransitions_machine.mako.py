# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1736535283.8405094
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
        agent_name = context.get('agent_name', UNDEFINED)
        transitions = context.get('transitions', UNDEFINED)
        states = context.get('states', UNDEFINED)
        initial_state = context.get('initial_state', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\nfrom transitions import State\r\nfrom transitions.extensions import GraphMachine\r\n\r\n\r\nclass ')
        __M_writer(str(agent_name))
        __M_writer('(GraphMachine):\r\n\r\n    def __init__(self, model) -> None:\r\n        """Constructor of the base `')
        __M_writer(str(agent_name))
        __M_writer('` class.\r\n        """\r\n')
        for state in states:
            __M_writer('        ')
            __M_writer(str(state))
            __M_writer(" = State(\r\n            name='")
            __M_writer(str(state))
            __M_writer("',\r\n        )\r\n")
        __M_writer('\r\n        states = ')
        __M_writer(str(states))
        __M_writer('\r\n\r\n        transitions = [\r\n')
        for transition in transitions:
            __M_writer('            ')
            __M_writer(str(transition))
            __M_writer(',\r\n')
        __M_writer('        ]\r\n\r\n        super().__init__(\r\n            model=model,\r\n            states=states,\r\n            transitions=transitions,\r\n            initial=')
        __M_writer(str(initial_state))
        __M_writer(',\r\n        )\r\n\r\n    def __getattr__(self, item):\r\n        """Method to get unlisted attributes of the class. If the attribute\r\n        is not found, the method will return the class attribute.\r\n\r\n        Args:\r\n            item: The class attribute that should be retrieved.\r\n\r\n        Returns:\r\n            The class attribute.\r\n        """\r\n        self.model.__getattribute__(item)\r\n\r\n    def next_state(self):\r\n        """Method for automatic execution of available transitions in each\r\n        of the machine states.\r\n        """\r\n        available_transitions = self.get_triggers(self.state)\r\n        available_transitions = available_transitions[len(self.states):]\r\n\r\n        LOGGER.debug(f\'Available transitions: {available_transitions}\')\r\n\r\n        for curr_transition in available_transitions:\r\n            may_method_result = self.may_trigger(curr_transition)\r\n            if may_method_result:\r\n                LOGGER.debug(f\'Transition executed: {curr_transition}\')\r\n                self.trigger(curr_transition)\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "src/adapter/templates/pytransitions_machine.mako", "uri": "src/adapter/templates/pytransitions_machine.mako", "source_encoding": "utf-8", "line_map": {"16": 1, "17": 2, "18": 3, "19": 4, "20": 0, "29": 3, "30": 8, "31": 8, "32": 11, "33": 11, "34": 13, "35": 14, "36": 14, "37": 14, "38": 15, "39": 15, "40": 18, "41": 19, "42": 19, "43": 22, "44": 23, "45": 23, "46": 23, "47": 25, "48": 31, "49": 31, "55": 49}}
__M_END_METADATA
"""
