from adapter.xml.uppaal_adapter import UppaalAdapter

from utils.utils import get_input_file

class ModelFactory:
    
    def __init__(self):
        self.model = ''
    
    def xml_model_factory(self, type) -> None:
        
        args = get_input_file()
        
        if type == 'uppaal':
            self.model = UppaalAdapter()
            root = self.model.parse_xml(args.input_file)
            states,transitions = self.model.get_xml_data(root)
            self.model.print_dict(states)
            self.model.print_dict(transitions)
        elif type == 'astah':
            raise NotImplementedError('')