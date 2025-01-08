from adapter.xml.adapter import Adapter
import xml.etree.ElementTree as ET

class UppaalAdapter(Adapter):
    
    # def __init__(self, input_file: str):
    #     super().__init__(input_file)
    
    # {
    #     states: [a,b,c],
    #     transitions: {
    #         {
    #             'trigger': f'{source_name}_to_{target_name}',
    #             'source': source_name,
    #             'dest': target_name,
    #         }
    #     }    
    # }
        

    def parse_xml(self, arg_to_parse: str) -> ET.Element:
        """function to get the root element from input file passed by argument

        Args:
            arg_to_parse (str)

        Returns:
            ET.Element
        """        
        tree = ET.parse(arg_to_parse)
        root = tree.getroot()
        return root
    
    def get_xml_data(self, root: ET.Element) -> tuple[dict,dict]:
        """function to return states and transitions from xml

        Args:
            root (ET.Element)

        Returns:
            tuple[dict,dict]
        """        
        states_dict = {}
        transitions_dict = {}
        # result = {}
        for template in root.findall(".//template"):
            agent_name = template.find('name').text
            states_dict[agent_name] = []
            transitions_dict[agent_name] = []
            # result[agent_name] = {}
            id_to_state = {}

            for location in template.findall('location'):
                state_id = location.get('id')
                state_name = location.find('name').text
                id_to_state[state_id] = state_name  
                states_dict[agent_name].append(state_name)

            for transition in template.findall('transition'):
                source_id = transition.find('source').get('ref')
                target_id = transition.find('target').get('ref')
                source_name = id_to_state.get(source_id)
                target_name = id_to_state.get(target_id)
                
                transitions_dict[agent_name].append({
                    'trigger': f'{source_name}_to_{target_name}',
                    'source': source_name,
                    'dest': target_name,
                })
        return states_dict, transitions_dict
            
    
    def print_dict(self, dict: dict) -> None:
        """function to print dict

        Args:
            dict (dict)
        """        
        for agent,_ in dict.items():
            print(f'agent: {agent}')
            print(f'{_}\n')