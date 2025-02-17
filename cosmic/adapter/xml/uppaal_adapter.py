import re
import xml.etree.ElementTree as ET

from cosmic.adapter.xml.adapter import Adapter
from cosmic.adapter.entities.machine_template import (
    State,
    Transition,
    MachineTemplate,
)
from cosmic.utils.string_oper import generate_function_name, to_snake_case
from functools import reduce

from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class UppaalAdapter(Adapter):
    """Adapter for Uppaal xml files. This class is responsible for parsing
    the xml file and extracting the necessary data into the general format
    that the Cosmic framework uses.
    """

    @staticmethod
    def find_xml_root(xml_file: str) -> ET.Element:
        # documentations provided by the `Adapter` base class
        tree = ET.parse(xml_file)
        root = tree.getroot()
        return root

    @staticmethod
    def declare_functions(
        conditions: List[str],
        unless: List[str],
    ) -> Dict[str, List[str]]:
        """Filters the function names from the conditions and unless
        lists, returning a dictionary with each of the declared functions,
        and the anonymous functions converted to function names. Those
        should be implemented at the machine model.

        Args:
            conditions (List[str]): The list of conditions.
            unless (List[str]): The list of unless conditions.

        Returns:
            Dict[str, List[str]]: A dictionary containing the declared
                functions.
        """

        is_function = r"^\s*\w+\s*\(.*\)\s*$"
        declared_functions = set()
        result_dict = defaultdict(list)
        for condition in conditions:
            if re.match(is_function, condition):
                f_name = condition.split("(")[0].strip()
                f_name = to_snake_case(f_name)
                declared_functions.add(f_name)
                result_dict["conditions"].append(f_name)
            else:
                f_name = generate_function_name(condition)
                f_name = to_snake_case(f_name)
                if f_name not in declared_functions:
                    result_dict["conditions"].append(f_name)
                    declared_functions.add(f_name)
        for declaration in unless:
            if re.match(is_function, declaration):
                f_name = declaration.split("(")[0].strip()
                f_name = to_snake_case(f_name)
                declared_functions.add(f_name)
                result_dict["unless"].append(f_name)
            else:
                f_name = generate_function_name(declaration)
                f_name = to_snake_case(f_name)
                if f_name not in declared_functions:
                    result_dict["unless"].append(f_name)
                    declared_functions.add(f_name)
        result_dict["declared_functions"] = list(declared_functions)
        return dict(result_dict)

    @staticmethod
    def filter_conditions(label_text: str) -> Dict[str, List[str]]:
        # documentations provided by the `Adapter` base class
        conditions = list()
        unless = list()

        guards_sublists = [guard.split("||")
                           for guard in label_text.split("&&")]
        guards = reduce(
            lambda acc, curr: acc.extend(curr) or acc,
            guards_sublists,
            list(),
        )
        for guard in guards:
            text = guard.strip()
            if text.startswith("!"):
                unless.append(text[1:])
            else:
                conditions.append(text)

        declared_functions_dict = UppaalAdapter.declare_functions(
            conditions,
            unless,
        )

        return declared_functions_dict

    @staticmethod
    def filter_updates(label_text: str) -> Dict[str, List[str]]:
        """Process the label text to find each of its declared updates,
        returning a dictionary with each of them.

        Args:
            label_text (str): The label text to be processed.

        Returns:
            Dict[str, List[str]]: A dictionary containing the updates.
        """
        updates = [updt.strip() for updt in label_text.split(",")]
        result_dict = UppaalAdapter.declare_functions(updates, [])
        return {
            "after": result_dict["conditions"],
            "declared_functions": result_dict["declared_functions"],
        }

    @staticmethod
    def evaluate_transition(
        transition: ET.Element,
    ) -> Tuple[
        bool,
        Dict[str, List[str]],
    ]:
        """Evaluates a given transition to understand if it has any labels,
        and where in the transition structure they should be placed.
        Returns a Tuple, containing two elements.
        The first element is a boolean indicating if the transition has a
        label.
        The second one is a dictionary with each of the found transition labels
        processed, along with the declared functions.

        Args:
            transition (ET.Element): The transition XML element.

        Returns:
            Tuple[bool, Dict[str, List[str]]]: A tuple containing a boolean
                indicating if the transition has a label, and a dictionary
                containing the processed labels.
        """
        has_label = False
        content = None

        transition_labels = transition.findall("label")
        if len(transition_labels) == 0:
            return has_label, content

        has_label = True
        content = dict()
        declared_functions = set()
        for label in transition_labels:
            if label.get("kind") == "guard":
                result_dict = UppaalAdapter.filter_conditions(label.text)
                for key, value in result_dict.items():
                    content[key] = value
                declared_functions.update(result_dict["declared_functions"])
            if label.get("kind") == "assignment":
                result_dict = UppaalAdapter.filter_updates(label.text)
                content["after"] = result_dict["after"]
                declared_functions.update(result_dict["declared_functions"])

        return has_label, content

    @staticmethod
    def find_branchpoint_target(
        branchpoint_id: str,
        edges_list: List[ET.Element],
    ) -> List[ET.Element]:
        """Finds all the targets of a given branchpoint id in a list of
        edges.

        Args:
            branchpoint_id (str): The branchpoint id to be searched.
            edges_list (List[ET.Element]): The list of edges in the xml file.

        Returns:
            List[ET.Element]: A list of the target elements of the given
                branchpoint id.
        """
        targets = list(filter(
            lambda x: x.find('source').get('ref') == branchpoint_id,
            edges_list,
        ))
        return targets

    @staticmethod
    def build_transition(
        id_to_state_map: Dict[str, str],
        edge: ET.Element,
        source_id: Optional[str] = None,
        target_state_id: Optional[str] = None,
    ) -> Transition:
        """Builds a transition object from the given parameters.

        Args:
            id_to_state_map (Dict[str, str]): A dictionary mapping the state
                ids to their names.
            edge (ET.Element): The edge element.
            source_id (Optional[str]): The source state id. Defaults to None.
                If not informed, the source state id will be extracted from
                the edge element.
            target_state_id (Optional[str]): The target state id. Defaults to
                None. If not informed, the target state id will be extracted
                from the edge element.

        Returns:
            Transition: A Transition object.
        """
        if source_id is None:
            source_id = edge.find("source").get("ref")
        if target_state_id is None:
            target_state_id = edge.find("target").get("ref")
        source_name = id_to_state_map.get(source_id)
        target_name = id_to_state_map.get(target_state_id)
        has_label, content = UppaalAdapter.evaluate_transition(
                            edge,
                        )
        transition = Transition(
                            trigger=f"{source_name}_to_{target_name}",
                            source=source_name,
                            dest=target_name,
                        )
        if has_label:
            for key, value in content.items():
                transition[key] = value
        return transition

    @staticmethod
    def parse_transitions(
        id_to_state: Dict[str, str],
        element_transitions: List[ET.Element],
        element_branchpoints: List[ET.Element] = list(),
    ) -> List[Transition]:
        """Parses the transitions from the xml file, returning a list of
        Transition objects.

        Args:
            id_to_state (Dict[str, str]): A dictionary mapping the state ids
            to their names.
            element_transitions (List[ET.Element]): The list of transitions
                in the xml file.
            element_branchpoints (List[ET.Element]): The list of branchpoints.
                Defaults to an empty list.

        Returns:
            List[Transition]: A list of Transition objects.
        """
        transitions_list = list()
        branchpoint_ids = [bp.get("id") for bp in element_branchpoints]

        visited_pairs = set()
        for tr in element_transitions:
            source_id = tr.find("source").get("ref")
            target_id = tr.find("target").get("ref")
            if (source_id, target_id) not in visited_pairs:
                visited_pairs.add((source_id, target_id))
                if target_id in branchpoint_ids:
                    target_edges = UppaalAdapter.find_branchpoint_target(
                        target_id,
                        element_transitions,
                    )
                    for edge in target_edges:
                        branch_target_id = edge.find("target").get("ref")
                        visited_pairs.add((target_id, branch_target_id))
                        transition = UppaalAdapter.build_transition(
                            id_to_state_map=id_to_state,
                            edge=edge,
                            source_id=source_id,
                            target_state_id=branch_target_id,
                        )
                        transitions_list.append(transition)
                elif source_id in branchpoint_ids:
                    continue
                else:
                    transition = UppaalAdapter.build_transition(
                        id_to_state_map=id_to_state,
                        edge=tr,
                        source_id=source_id,
                        target_state_id=target_id,
                    )
                    transitions_list.append(transition)
        return transitions_list

    @staticmethod
    def parse_template(template: ET.Element) -> MachineTemplate:
        locations = template.findall('location')
        transitions = template.findall('transition')
        branchpoints = template.findall('branchpoint')

        id_state_map = dict()
        states = list()
        for loc in locations:
            state_name = to_snake_case(loc.find('name').text)
            state_id = loc.get('id')
            # not handling on_enter and on_exit actions yet
            state = State(name=state_name)
            id_state_map[state_id] = state_name
            states.append(state)

        transitions_list = UppaalAdapter.parse_transitions(
            id_to_state=id_state_map,
            element_transitions=transitions,
            element_branchpoints=branchpoints,
        )

        return MachineTemplate(
            initial_state=states[0]['name'],
            states=states,
            transitions=transitions_list,
        )

    @staticmethod
    def get_xml_data(xml_file: str) -> Dict[str, MachineTemplate]:
        # documentations provided by the `Adapter` base class
        root = UppaalAdapter.find_xml_root(xml_file)
        result = {}

        for template in root.findall(".//template"):
            # parse template
            agent_name = (template.find("name").text).replace("_", "")
            machine_template = UppaalAdapter.parse_template(template)
            result[agent_name] = machine_template

        return result

    @staticmethod
    def print_dict(result_dict: dict) -> None:  # pragma: no cover
        # documentations provided by the `Adapter` base class
        for agent, _agent_data in result_dict.items():
            print(f"agent: {agent}")
            print(f"{_agent_data}\n")
