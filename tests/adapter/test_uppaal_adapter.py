import pytest
import xml.etree.ElementTree as ET
from cosmic.adapter.xml.uppaal_adapter import UppaalAdapter


@pytest.fixture
def transition_element() -> ET.Element:
    transition = ET.Element('transition', id='id15')
    ET.SubElement(transition, 'source', ref='1d6')
    ET.SubElement(transition, 'target', ref='1d9')

    guard_label = ET.SubElement(
        transition,
        "label",
        kind="guard",
        x="-1088",
        y="-382",
    )
    guard_label.text = "!activated() && x == 0 || force_stop()"
    sync_label = ET.SubElement(
        transition,
        "label",
        kind="update",
        x="-1071",
        y="-348",
    )
    sync_label.text = "y = 0, in_op = false, reset_queue()"
    ET.SubElement(transition, "nail", x="-790", y="-331")
    return transition


@pytest.fixture
def simple_transition_element() -> ET.Element:
    transition = ET.Element('transition', id='id15')
    ET.SubElement(transition, 'source', ref='1d6')
    ET.SubElement(transition, 'target', ref='1d9')
    return transition


def test_find_xml_root(xml_file):
    root = UppaalAdapter.find_xml_root(xml_file)
    assert root.tag == 'nta'


@pytest.mark.parametrize(
        'conditions, unless, expected',
        [
            (
                [
                    "place < buffer[rid].length",
                    "time <= time_buffer",
                ],
                [],
                {
                    "conditions": ["place_eval", "time_eval"],
                    "declared_functions": ["time_eval", "place_eval"],
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
                    "conditions": ["dependencies_met", "retry_eval"],
                    "unless": ["halt_op"],
                    "declared_functions": [
                        "dependencies_met",
                        "retry_eval",
                        "halt_op",
                    ],
                }
            ),
            (
                ["dependencies_met()", "retry > 3"],
                ["time <= time_buffer"],
                {
                    "conditions": ["dependencies_met", "retry_eval"],
                    "unless": ["time_eval"],
                    "declared_functions": [
                        "dependencies_met",
                        "retry_eval",
                        "time_eval",
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
                "place < buffer[rid].length && time <= time_buffer",
                {
                    "conditions": ["place_eval", "time_eval"],
                    "declared_functions": ["time_eval", "place_eval"],
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
                    "conditions": ["dependencies_met", "retry_eval"],
                    "unless": ["halt_op"],
                    "declared_functions": [
                        "dependencies_met",
                        "retry_eval",
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


def test_evalute_transition_without_labels(simple_transition_element):
    has_label, content = UppaalAdapter.evaluate_transition(
        simple_transition_element,
    )
    assert not has_label
    assert content is None


def test_evaluate_transition(transition_element):
    has_label, content = UppaalAdapter.evaluate_transition(transition_element)
    # bad test assertion, but dictionaries...
    assert has_label
    assert set(content.keys()) == {
        'conditions', 'unless', 'after', 'declared_functions',
    }
    assert content['conditions'] == ['x_eval', 'force_stop']
    assert content['unless'] == ['activated']
    assert content['after'] == ['y_eval', 'in_op_eval', 'reset_queue']


def test_get_xml_data(xml_file):
    result_dict = UppaalAdapter.get_xml_data(xml_file)
    expected_agents = {'RobotAssembler', 'HumanReceiver',
                       'HumanValidator', 'Sector', 'RobotDeliver'}
    assert set(result_dict.keys()) == expected_agents
