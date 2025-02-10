import re
import xml.etree.ElementTree as ET

from cosmic.adapter.xml.adapter import Adapter
from cosmic.utils.string_oper import generate_function_name
from functools import reduce

from typing import Dict, List, Tuple
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
                declared_functions.add(f_name)
                result_dict["conditions"].append(f_name)
            else:
                f_name = generate_function_name(condition)
                if f_name not in declared_functions:
                    result_dict["conditions"].append(f_name)
                    declared_functions.add(f_name)
        for declaration in unless:
            if re.match(is_function, declaration):
                f_name = declaration.split("(")[0].strip()
                declared_functions.add(f_name)
                result_dict["unless"].append(f_name)
            else:
                f_name = generate_function_name(declaration)
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
            if label.get("kind") == "update":
                result_dict = UppaalAdapter.filter_updates(label.text)
                content["after"] = result_dict["after"]
                declared_functions.update(result_dict["declared_functions"])

        return has_label, content

    @staticmethod
    def get_xml_data(xml_file: str) -> dict:
        # documentations provided by the `Adapter` base class
        root = UppaalAdapter.find_xml_root(xml_file)
        result = {}

        for template in root.findall(".//template"):
            agent_name = (template.find("name").text).replace("_", "")
            result[agent_name] = {
                "initial_state": "",
                "states": [],
                "transitions": [],
            }
            id_to_state = {}
            states = []

            for location in template.findall("location"):
                state_id = location.get("id")
                state_name = location.find("name").text
                states.append(state_name)
                id_to_state[state_id] = state_name
                result[agent_name]["states"].append(state_name)
                result[agent_name]["initial_state"] = states[0]

            for transition in template.findall("transition"):
                # might have selections, guards, synchronisation,
                # updates, and weights
                # - synchronisations not handled yet
                # - selections might not be included in the code,
                # probably being used only by the model
                # - updates can be translated to `after` in transitions
                source_id = transition.find("source").get("ref")
                target_id = transition.find("target").get("ref")
                source_name = id_to_state.get(source_id)
                target_name = id_to_state.get(target_id)
                has_label, content = UppaalAdapter.evaluate_transition(
                    transition,
                )

                transition = {
                        "trigger": f"{source_name}_to_{target_name}",
                        "source": source_name,
                        "dest": target_name,
                    }
                if has_label:
                    # The declared functions must be implemented in the
                    # machine model.
                    if 'declared_functions' in content.keys():
                        del content['declared_functions']
                    for key, value in content.items():
                        transition[key] = value
                result[agent_name]["transitions"].append(transition)

        return result

    @staticmethod
    def print_dict(result_dict: dict) -> None:  # pragma: no cover
        # documentations provided by the `Adapter` base class
        for agent, _agent_data in result_dict.items():
            print(f"agent: {agent}")
            print(f"{_agent_data}\n")
