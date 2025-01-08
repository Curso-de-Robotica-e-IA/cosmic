from abc import abstractmethod, ABC

class Adapter(ABC):
    
    # def __init__(self, input_file: str):
    #     self.input_file = input_file
        
    @abstractmethod
    def parse_xml(self, arg_to_parse):
        raise NotImplementedError('')

    @abstractmethod
    def get_xml_data(self, root):
        raise NotImplementedError('')

    @abstractmethod
    def print_dict(self, dict):
        raise NotImplementedError('')

