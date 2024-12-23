import json
import tempfile
import typing
from pathlib import Path

import click
from rich.console import Console

from py_templating_engine.environment import TemplatesEnvironment
from py_templating_engine.renderer import Renderer

console = Console()


@click.command()
@click.option("-t", "--template-dir", type=str, help="Template directory.")
@click.option(
    "-o",
    "--output-dir",
    type=str,
    help="Output generated project dir.",
)
def main(
    template_dir: str,
    output_dir: str,
) -> None:
    """Get arguments from command line and generate project."""
    if not (template_dir or output_dir):
        console.print(
            "[bold red]You need to provide template and output directory!"
            "[/bold red]",
        )
    else:
        console.print(
            f"[bold cyan]Starting generating project to {output_dir} "
            f"dir[/bold cyan]",
        )
        context: dict[str, typing.Any] = get_current_context(template_dir)

        with (
            tempfile.TemporaryDirectory(
                ignore_cleanup_errors=True,
            ) as temp_dir,
            Path(f"{temp_dir}/temp_file.txt").open("w+t") as tmp_context_file,
        ):
            json.dump(context, tmp_context_file)
            tmp_context_file.flush()
            tmp_context_file.seek(0)
            environment = TemplatesEnvironment(template_dir)
            environment.render_project(
                output_dir=output_dir,
                create_dirs=True,
                context_path=tmp_context_file.name,
            )
        console.print("[bold green]Project successfully created![/bold green]")


def get_current_context(template_dir: str) -> dict[str, typing.Any]:
    context = Renderer.load_context(Path("templater.json"))
    for variable, value in context.items():
        console.print(
            f"Enter {variable} value (default = [bold yellow]"
            f"{value}[/bold yellow]): ",
            end="",
        )
        new_value = input()
        context[variable] = new_value if new_value else value
    return context


if __name__ == "__main__":  # pragma: no cover
    main()
