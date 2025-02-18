from pathlib import Path
from rich import print
from rich.console import Console
from typer import Context, Exit, Option, Typer
from rich.traceback import install
from cosmic.generator.code_generator import CodeGenerator


app = Typer()
console = Console()
install(show_locals=True)


def version_callback(value: bool):
    if value:
        console.print('COSMIC v0.1.0')
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(None, '--version', callback=version_callback, is_eager=True),  # noqa
    xml: str = Option('uppaal', '--xml', '-x', help='The tool from which the XML file was generated'),  # noqa
    code: str = Option('pytransitions', '--code', '-c', help='The dialect of the code to be generated'),  # noqa
    output: str = Option(..., '--output', '-o', help='The output directory for the generated code'),  # noqa
    input: str = Option(..., '--input', '-i', help='The path to the XML file'),  # noqa
    generate_model: bool = Option(True, '--generate-model', '-m', help='Generate the model file'),  # noqa
):
    if ctx.invoked_subcommand:
        return
    try:
        console.log('[bold]Welcome to COSMIC. Initializing...[/bold]')
        input_file = Path(input)
        output_dir = Path(output)
        if not (input_file.exists() and input_file.is_file()):
            console.log(f'[red]File not found: {input_file}[/red]')
            return
        cg = CodeGenerator(
            code_dialect=code,
            xml_dialect=xml,
            generate_model=generate_model,
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
