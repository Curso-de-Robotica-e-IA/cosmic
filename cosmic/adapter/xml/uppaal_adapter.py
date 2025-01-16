import xml.etree.ElementTree as ET
from cosmic.adapter.xml.adapter import Adapter


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
    def filter_conditions(declaration: str) -> list:
        # documentations provided by the `Adapter` base class
        function_names = []

        for line in declaration.splitlines():
            line = line.strip()
            if line.startswith("bool"):

                name = line.split()[1].split("(")[0]
                function_names.append(name)

        return function_names

    @staticmethod
    def get_xml_data(xml_file: str) -> dict:
        # documentations provided by the `Adapter` base class
        root = UppaalAdapter.find_xml_root(xml_file)
        result = {}

        for template in root.findall(".//template"):
            agent_name = template.find("name").text
            result[agent_name] = {
                "initial_state": "",
                "states": [],
                "transitions": [],
            }
            id_to_state = {}
            states = []

            for declaration in template.findall("declaration"):
                condition = declaration.text
                filtered_conditions = UppaalAdapter.filter_conditions(
                    condition,
                )

            for location in template.findall("location"):
                state_id = location.get("id")
                state_name = location.find("name").text
                states.append(state_name)
                id_to_state[state_id] = state_name
                result[agent_name]["states"].append(state_name)
                result[agent_name]["initial_state"] = states[0]

            for transition in template.findall("transition"):
                source_id = transition.find("source").get("ref")
                target_id = transition.find("target").get("ref")
                source_name = id_to_state.get(source_id)
                target_name = id_to_state.get(target_id)

                transition = {
                        "trigger": f"{source_name}_to_{target_name}",
                        "source": source_name,
                        "dest": target_name,
                    }
                if len(filtered_conditions) > 0:
                    transition["conditions"] = filtered_conditions
                result[agent_name]["transitions"].append(transition)

        return result

    @staticmethod
    def print_dict(result_dict: dict) -> None:
        # documentations provided by the `Adapter` base class
        for agent, _agent_data in result_dict.items():
            print(f"agent: {agent}")
            print(f"{_agent_data}\n")
