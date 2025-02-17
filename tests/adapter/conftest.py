import pytest
import xml.etree.ElementTree as ET
from pathlib import Path


@pytest.fixture
def uppal_transition_element() -> ET.Element:
    """Fixture to return a transition element with guards and updates.
    """
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
        kind="assignment",
        x="-1071",
        y="-348",
    )
    sync_label.text = "y == 0, in_op == false, reset_queue()"
    ET.SubElement(transition, "nail", x="-790", y="-331")
    return transition


@pytest.fixture
def uppal_simple_transition_element() -> ET.Element:
    """Fixture to return a simple transition element.
    """
    transition = ET.Element('transition', id='id15')
    ET.SubElement(transition, 'source', ref='1d6')
    ET.SubElement(transition, 'target', ref='1d9')
    return transition


@pytest.fixture
def uppaal_branchpoint_machine() -> ET.Element:
    """Fixture to return an UPPAL Template with a branchpoint and some
    transitions.

    This fixture depends on the file
    `tests/mock_files/branchpoint_machine.xml`.
    """
    xml_path = Path('tests\\mock_files\\branchpoint_machine.xml')
    assert xml_path.exists() and xml_path.is_file()
    tree = ET.parse(xml_path)
    root = tree.getroot()
    template = root.findall('.//template')[0]
    return template
