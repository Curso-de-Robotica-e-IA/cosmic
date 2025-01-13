from argparse import ArgumentParser
from pathlib import Path
from rich import print
from rich.console import Console
from rich.traceback import install
from generator.code_generator import CodeGenerator


def main():
    cg = CodeGenerator(
        code_dialect='pytransitions',
        xml_dialect='uppaal'
    )
    xml_path = Path(
        'tests',
        'mock_files',
        'hcl_teste.xml',
    )
    cg.generate_code(
        xml_file=xml_path,
        output_dir=Path('generated_code'),
    )


def initialize_parser() -> ArgumentParser:
    """Initialize the argument parser for the code generator.

    Returns:
        ArgumentParser: The argument parser for the code generator.
    """
    description = 'Generates python finite state machine code from an xml file'
    parser = ArgumentParser(
        prog='COSMIC: Code Generator',
        usage='cosmic [options] [args]',
        description=description,
        add_help=True,
        exit_on_error=True,
    )

    parser.add_argument(
        '--xml',
        '-x',
        type=str,
        help='The tool from which the XML file was generated',
        required=False,
    )
    parser.add_argument(
        '--code',
        '-c',
        type=str,
        help='The dialect of the code to be generated',
        required=False,
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='The output directory for the generated code',
        required=True,
    )
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        help='The path to the XML file',
        required=True,
    )
    return parser


if __name__ == '__main__':
    install(
        show_locals=True,
    )
    console = Console()
    parser = initialize_parser()

    args = parser.parse_args()
    try:
        console.log('[bold]Welcome to COSMIC. Initializing...[/bold]')
        input_file = Path(args.input)
        output_dir = Path(args.output)
        code = args.code
        if code is None:
            code = 'pytransitions'
        xml = args.xml
        if xml is None:
            xml = 'uppaal'
        if not (input_file.exists() and input_file.is_file()):
            console.log(f'[red]File not found: {input_file}[/red]')
        cg = CodeGenerator(
            code_dialect=code,
            xml_dialect=xml,
        )
        console.log(
            f'COSMIC Initialized using [code]{xml}[/code] and [code]{code}[/code].',  # noqa
            markup=True,
        )
        console.log(
            f'Reading FSMs from [code]{input_file}[/code].',
            markup=True,
        )
        console.log(
            f'Generating code in [code]{output_dir}[/code].',
            markup=True,
        )
        cg.generate_code(
            xml_file=input_file,
            output_dir=output_dir,
        )
        console.log('[bold]Code generation completed![/bold]')
    except Exception as e:
        print(f'[red]{e}[/red]')
