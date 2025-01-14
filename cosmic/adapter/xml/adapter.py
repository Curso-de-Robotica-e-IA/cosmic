from abc import abstractmethod, ABC
import xml.etree.ElementTree as ET


class Adapter(ABC):

    @abstractmethod
    def parse_xml(self, arg_to_parse: str) -> ET.Element:
        """function to get the root element from input file passed by argument

        Args:
            arg_to_parse (str)

        Returns:
            ET.Element
        """
        raise NotImplementedError()

    @abstractmethod
    def get_xml_data(self, root: ET.Element) -> dict:
        """function to return states and transitions from xml

        Args:
            root (ET.Element)

        Returns:
            tuple[dict,dict]
        """
        raise NotImplementedError()

    @abstractmethod
    def print_dict(self, result_dict: dict) -> None:
        """function to print dict

        Args:
            result_dict (dict)
        """
        raise NotImplementedError()

    @abstractmethod
    def filter_conditions(self, declaration: str) -> list:
        """function to extract function names from xml

        Args:
            declaration (str)

        Returns:
            list
        """
        raise NotImplementedError()
