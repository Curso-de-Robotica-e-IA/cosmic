from cosmic.adapter.xml.adapter import Adapter
from cosmic.adapter.xml.uppaal_adapter import UppaalAdapter
from typing import Literal


DIALECTS = Literal["uppaal", "astah"]


class ModelFactory:

    @staticmethod
    def xml_model_factory(dialect: DIALECTS) -> Adapter:
        """factory to decide which model will be parsed

        Args:
            dialect (DIALECTS): which is the program source for the xml file.

        Raises:
            NotImplementedError
        """

        if dialect == "uppaal":
            return UppaalAdapter()
        elif dialect == "astah":
            raise NotImplementedError("Type not supported yet.")
