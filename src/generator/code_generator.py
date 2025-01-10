from src.adapter.xml.model_factory import (
    ModelFactory,
    DIALECTS as XML_DIALECTS,
)
from mako.template import Template
from pathlib import Path
from typing import Literal, Union


DIALECTS = Literal['pytransitions', 'python-state-machine']


class CodeGenerator:
    """Class to generate a finite state machine python code from a xml file.
    """

    @staticmethod
    def get_template_file(code_dialect: DIALECTS):
        """Return the template file for the code generation.

        Args:
            code_dialect (DIALECTS): The dialect of the code to be generated.

        Raises:
            NotImplementedError: If the dialect is not supported.

        Returns:
            file: The template file for the code generation.
        """
        ref_files = {
            'pytransitions': Path('src', 'adapter', 'templates', 'pytransitions_machine.mako'), # noqa
        }
        if code_dialect not in ref_files.keys():
            raise NotImplementedError('Type not supported yet.')
        return ref_files.get(code_dialect)

    def __init__(
        self,
        xml_dialect: XML_DIALECTS,
        code_dialect: DIALECTS,
    ) -> None:
        self.xml_adapter = ModelFactory.xml_model_factory(xml_dialect)
        self.template_file = self.get_template_file(code_dialect)
        self.template = Template(
            filename=self.template_file.as_posix(),
            module_directory='src/generator/tmp/mako_modules',
        )

    def generate_code(
        self,
        xml_file: Union[Path, str],
        output_dir: Path,
    ) -> None:
        """Generate code from the xml file.
        From the xml file input, uses the adapter to parse the content into a
        result dictionary containing one or more agents, which will be each
        converted into a python file containing the finite state machine code
        for its logic.

        Args:
            xml_file (Union[Path, str]): The xml file to be parsed.
            output_dir (Path): The directory where the output files will be
                saved.

        Raises:
            FileNotFoundError: If the xml file is not found.
        """
        if isinstance(xml_file, str):
            xml_file = Path(xml_file)
        if not xml_file.exists() or not xml_file.is_file():
            raise FileNotFoundError(f'File {xml_file} not found.')

        root = self.xml_adapter.parse_xml(xml_file.resolve())
        result_dict = self.xml_adapter.get_xml_data(root)

        for agent_name, data in result_dict.items():
            output_file = Path(output_dir).joinpath(f'{agent_name}.py')

            with open(output_file, 'w') as file:
                file.write(
                    self.template.render(
                        agent_name=agent_name,
                        **data,
                    ),
                )