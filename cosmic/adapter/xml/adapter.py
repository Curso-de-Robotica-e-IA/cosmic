from abc import abstractmethod, ABC
import xml.etree.ElementTree as ET


class Adapter(ABC):

    @staticmethod
    @abstractmethod
    def find_xml_root(self, xml_file: str) -> ET.Element:
        """Find the root of the xml file

        Args:
            xml_file (str): Path to the xml file.

        Returns:
            ET.Element: The root of the xml file.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_xml_data(self, xml_file: str) -> dict:
        """Extract the necessary data from the xml file, creating a dictionary
        used to create state machines in the expected Cosmic framework format.

        Args:
            xml_file (str): Path to the xml file.

        Returns:
            dict: A dictionary containing the necessary data to create state
                machines in the Cosmic framework format.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def print_dict(self, result_dict: dict) -> None:
        """Print the result dictionary in a human-readable format.

        Args:
            result_dict (dict): The result dictionary to be printed.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def filter_conditions(self, declaration: str) -> list:
        """Filter the conditions from the declaration, returning a list of
        function names.

        Args:
            declaration (str): The declaration of the xml file.

        Returns:
            list: A list of function names.
        """
        raise NotImplementedError()
