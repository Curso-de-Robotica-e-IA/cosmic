from src.adapter.xml.adapter import Adapter
import xml.etree.ElementTree as ET


class UppaalAdapter(Adapter):

    def parse_xml(self, arg_to_parse: str) -> ET.Element:
        tree = ET.parse(arg_to_parse)
        root = tree.getroot()
        return root

    def get_xml_data(self, root: ET.Element) -> dict:
        result = {}

        for template in root.findall(".//template"):
            agent_name = template.find("name").text
            result[agent_name] = {"states": [], "transitions": []}
            id_to_state = {}

            for location in template.findall("location"):
                state_id = location.get("id")
                state_name = location.find("name").text
                id_to_state[state_id] = state_name
                result[agent_name]["states"].append(state_name)

            for transition in template.findall("transition"):
                source_id = transition.find("source").get("ref")
                target_id = transition.find("target").get("ref")
                source_name = id_to_state.get(source_id)
                target_name = id_to_state.get(target_id)

                result[agent_name]["transitions"].append(
                    {
                        "trigger": f"{source_name}_to_{target_name}",
                        "source": source_name,
                        "dest": target_name,
                    }
                )

        return result

    def print_dict(self, result_dict: dict) -> None:
        for agent, _ in result_dict.items():
            print(f"agent: {agent}")
            print(f"{_}\n")
