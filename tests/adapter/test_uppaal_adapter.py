import pytest
from cosmic.adapter.xml.uppaal_adapter import UppaalAdapter
from cosmic.adapter.entities.machine_template import (
    MachineTemplate,
    State,
    Transition,
)


def test_find_xml_root(xml_file):
    root = UppaalAdapter.find_xml_root(xml_file)
    assert root.tag == 'nta'


@pytest.mark.parametrize(
        'conditions, unless, expected',
        [
            (
                [
                    "place < buffer_length",
                    "time <= time_buffer",
                ],
                [],
                {
                    "conditions": [
                        "place_lt_buffer_length", "time_lte_time_buffer",
                    ],
                    "declared_functions": [
                        "time_lte_time_buffer", "place_lt_buffer_length",
                    ],
                },
            ),
            (
                ["dependencies_met()", "is_valid()"],
                ["halt_op()"],
                {
                    "conditions": ["dependencies_met", "is_valid"],
                    "unless": ["halt_op"],
                    "declared_functions": [
                        "dependencies_met",
                        "is_valid",
                        "halt_op",
                    ],
                },
            ),
            (
                ["dependencies_met()", "retry > 3"],
                ["halt_op()"],
                {
                    "conditions": ["dependencies_met", "retry_gt_three"],
                    "unless": ["halt_op"],
                    "declared_functions": [
                        "dependencies_met",
                        "retry_gt_three",
                        "halt_op",
                    ],
                }
            ),
            (
                ["dependencies_met()", "retry > 3"],
                ["time <= time_buffer"],
                {
                    "conditions": ["dependencies_met", "retry_gt_three"],
                    "unless": ["time_lte_time_buffer"],
                    "declared_functions": [
                        "dependencies_met",
                        "retry_gt_three",
                        "time_lte_time_buffer",
                    ],
                }
            )
        ]
)
def test_declare_functions(conditions, unless, expected):
    result = UppaalAdapter.declare_functions(conditions, unless)
    assert result.keys() == expected.keys()
    # bad test assertion, but dictionaries...
    if expected.get('conditions'):
        assert result['conditions'] == expected['conditions']
    if expected.get('unless'):
        assert result['unless'] == expected['unless']
    if expected.get('declared_functions'):
        for func in expected['declared_functions']:
            assert func in result['declared_functions']


@pytest.mark.parametrize(
        'label_text, expected',
        [
            (
                "place < buffer_length && time <= time_buffer",
                {
                    "conditions": [
                        "place_lt_buffer_length", "time_lte_time_buffer",
                    ],
                    "declared_functions": [
                        "time_lte_time_buffer", "place_lt_buffer_length",
                    ],
                },
            ),
            (
                "dependencies_met() && is_valid() || !halt_op()",
                {
                    "conditions": ["dependencies_met", "is_valid"],
                    "unless": ["halt_op"],
                    "declared_functions": [
                        "dependencies_met",
                        "is_valid",
                        "halt_op",
                    ],
                },
            ),
            (
                "dependencies_met() && retry > 3 || !halt_op()",
                {
                    "conditions": ["dependencies_met", "retry_gt_three"],
                    "unless": ["halt_op"],
                    "declared_functions": [
                        "dependencies_met",
                        "retry_gt_three",
                        "halt_op",
                    ],
                }
            )
        ]
)
def test_filter_conditions(label_text, expected):
    result = UppaalAdapter.filter_conditions(label_text)
    assert result.keys() == expected.keys()
    # bad test assertion, but dictionaries...
    if expected.get('conditions'):
        assert result['conditions'] == expected['conditions']
    if expected.get('unless'):
        assert result['unless'] == expected['unless']
    if expected.get('declared_functions'):
        for func in expected['declared_functions']:
            assert func in result['declared_functions']


def test_evalute_transition_without_labels(uppaal_simple_transition_element):
    has_label, content = UppaalAdapter.evaluate_transition(
        uppaal_simple_transition_element,
    )
    assert not has_label
    assert content is None


def test_evaluate_transition(uppaal_transition_element):
    has_label, content = UppaalAdapter.evaluate_transition(
        uppaal_transition_element,
    )
    # bad test assertion, but dictionaries...
    assert has_label
    assert set(content.keys()) == {
        'conditions', 'unless', 'after', 'declared_functions',
    }
    assert content['conditions'] == ['x_eq_zero', 'force_stop']
    assert content['unless'] == ['activated']
    assert content['after'] == ['y_eq_zero', 'in_op_eq_false', 'reset_queue']


def test_get_xml_data(xml_file):
    result_dict = UppaalAdapter.get_xml_data(xml_file)
    expected_agents = {'RobotAssembler', 'HumanReceiver',
                       'HumanValidator', 'Sector', 'RobotDeliver'}
    assert set(result_dict.keys()) == expected_agents


def test_build_transition(uppaal_transition_element):
    id_to_state = {
        '1d1': 'state1',
        '1d2': 'state2',
        '1d3': 'state3',
        '1d4': 'state4',
        '1d5': 'state5',
        '1d6': 'state6',
        '1d7': 'state7',
        '1d8': 'state8',
        '1d9': 'state9',
    }

    expected = Transition(
        trigger='state6_to_state9',
        source='state6',
        dest='state9',
        conditions=['x_eq_zero', 'force_stop'],
        unless=['activated'],
        after=['y_eq_zero', 'in_op_eq_false', 'reset_queue'],
        declared_functions=[
            'x_eq_zero', 'force_stop', 'activated',
        ],
    )

    result = UppaalAdapter.build_transition(
        id_to_state_map=id_to_state,
        edge=uppaal_transition_element,
    )
    assert result.keys() == expected.keys()
    # bad test assertion, but dictionaries...
    for key in expected.keys():
        result_content = result[key]
        if isinstance(result_content, list):
            assert result_content.sort() == expected[key].sort()
        else:
            assert result_content == expected[key]


def test_parse_transitions(uppaal_branchpoint_machine):
    id_to_state = {
        'id0': 'start',
        'id1': 'decision',
        'id2': 'success',
        'id3': 'retry',
        'id4': 'finish',
    }
    transitions_list = uppaal_branchpoint_machine.findall('transition')
    branchpoints_list = uppaal_branchpoint_machine.findall('branchpoint')

    result = UppaalAdapter.parse_transitions(
        id_to_state=id_to_state,
        element_transitions=transitions_list,
        element_branchpoints=branchpoints_list,
    )

    expected = [
        Transition(
            trigger='start_to_decision',
            source='start',
            dest='decision',
        ),
        Transition(
            trigger='decision_to_retry',
            source='decision',
            dest='retry',
        ),
        Transition(
            trigger='decision_to_success',
            source='decision',
            dest='success',
        ),
        Transition(
            trigger='retry_to_decision',
            source='retry',
            dest='decision',
        ),
        Transition(
            trigger='success_to_finish',
            source='success',
            dest='finish',
        ),
    ]

    assert len(result) == len(expected)
    for result_transition in result:
        assert result_transition in expected


def test_parse_template(uppaal_branchpoint_machine):
    result = UppaalAdapter.parse_template(
        uppaal_branchpoint_machine,
    )
    expected = MachineTemplate(
        initial_state='start',
        states=[
            State(name='start'),
            State(name='decision'),
            State(name='success'),
            State(name='retry'),
            State(name='finish'),
        ],
        transitions=[
            Transition(
                dest='finish',
                source='success',
                trigger='success_to_finish',
            ),
            Transition(
                dest='decision',
                source='retry',
                trigger='retry_to_decision',
            ),
            Transition(
                dest='success',
                source='decision',
                trigger='decision_to_success',
            ),
            Transition(
                dest='retry',
                source='decision',
                trigger='decision_to_retry',
            ),
            Transition(
                dest='decision',
                source='start',
                trigger='start_to_decision',
            ),
        ]
    )

    assert result == expected


@pytest.mark.parametrize(
    'label_text, expected',
    [
        ('logState()', ['log_state']),
        ('reset()', ['reset']),
        ('logState(), reset()', ['log_state', 'reset']),
        (
            'logState(), reset(), snake_case()',
            ['log_state', 'reset', 'snake_case'],
        ),
    ]
)
def test_format_state_functions(label_text, expected):
    result = UppaalAdapter._format_state_functions(label_text)
    assert result == expected


def test_build_state(uppaal_state_element):
    result = UppaalAdapter.build_state(uppaal_state_element)
    expected_state = State(
        name='init',
        on_enter=['log_state', 'make_step_action'],
        on_exit=['log_exit'],
    )
    expected_functions = ['log_state', 'make_step_action', 'log_exit']
    result_state, result_functions = result
    for func in expected_functions:
        assert func in result_functions
    for key in expected_state.keys():
        assert result_state[key] == expected_state[key]
