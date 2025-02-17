import shutil

from cosmic.adapter.xml.model_factory import (
    ModelFactory,
    DIALECTS as XML_DIALECTS,
)
from cosmic.utils.string_oper import to_snake_case
from mako.template import Template
from pathlib import Path
from rich.progress import Progress
from typing import Literal, Union


DIALECTS = Literal["pytransitions", "python-state-machine"]
BASE_PATH = Path(__file__).resolve().parent.parent


class CodeGenerator:
    """Class to generate a finite state machine python code from a xml file."""

    temp_folder: Path = Path(BASE_PATH, "generator", "tmp", "mako_modules")

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
            "pytransitions": Path(
                BASE_PATH, "adapter", "templates", "pytransitions_machine.mako"
            ),
        }
        if code_dialect not in ref_files.keys():
            raise NotImplementedError("Type not supported yet.")
        return ref_files.get(code_dialect)

    @staticmethod
    def get_template_model_file(code_dialect: DIALECTS):
        """Return the template file for the code generation.

        Args:
            code_dialect (DIALECTS): The dialect of the code to be generated.

        Raises:
            NotImplementedError: If the dialect is not supported.

        Returns:
            file: The template file for the code generation.
        """
        ref_files = {
            "pytransitions": Path(
                BASE_PATH, "adapter", "templates", "pytransitions_model.mako"
            ),
        }
        if code_dialect not in ref_files.keys():
            raise NotImplementedError("Type not supported yet.")
        return ref_files.get(code_dialect)

    def __init__(
        self,
        xml_dialect: XML_DIALECTS,
        code_dialect: DIALECTS,
    ) -> None:
        self.xml_adapter = ModelFactory.xml_model_factory(xml_dialect)
        self.template_file = self.get_template_file(code_dialect)
        self.template_model_file = self.get_template_model_file(code_dialect)
        self.template = Template(
            filename=self.template_file.as_posix(),
            module_directory=self.temp_folder,
        )
        self.template_model = Template(
            filename=self.template_model_file.as_posix(),
            module_directory=self.temp_folder,
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
            raise FileNotFoundError(f"File {xml_file} not found.")

        result_dict = self.xml_adapter.get_xml_data(xml_file.resolve())

        if not output_dir.exists():
            output_dir.mkdir()

        with Progress() as progress:
            codegen = progress.add_task(
                "Generating code...",
                total=len(result_dict),
            )
            advance_amount = 100 / len(result_dict)
            for agent_name, data in result_dict.items():
                output_file = Path(output_dir).joinpath(
                    f"{to_snake_case(agent_name)}.py",
                )
                model_file = Path(output_dir).joinpath(
                    f"{to_snake_case(agent_name)}_model.py",
                )
                progress.update(
                    task_description=f"Generating code for {agent_name}...",
                    task_id=codegen,
                    advance=advance_amount,
                )
                with open(output_file, "w") as file:
                    file.write(
                        self.template.render(
                            agent_name=agent_name,
                            **data,
                        ),
                    )
                declared_functions = data.get("declared_functions", [])
                if len(declared_functions) > 0:
                    with open(model_file, "w") as mfile:
                        mfile.write(
                            self.template_model.render(
                                agent_name=agent_name,
                                declared_functions=declared_functions,
                            ),
                        )
        shutil.rmtree(self.temp_folder)
