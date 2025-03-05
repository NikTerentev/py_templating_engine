from pathlib import Path

from py_templating_engine import exceptions
from py_templating_engine.renderer import Renderer
from py_templating_engine.template import Template


class TemplatesEnvironment:
    def __init__(self, dir_path: Path) -> None:
        self.dir_path: Path = self._validate_path(dir_path)
        self.output_dir: Path = self._validate_path(dir_path.parent)

    def _validate_path(self, dir_path: Path) -> Path:
        if not dir_path.is_dir():
            raise exceptions.TemplatesDirNotFoundError(dir_path.name)
        if not any(dir_path.iterdir()):
            raise exceptions.TemplatesDirIsEmpty(dir_path.name)
        return dir_path

    def get_template(self, template_name: str) -> Template:
        return Template((self.dir_path / Path(template_name)).as_posix())

    def render_project(
        self,
        context_path: str = "",
    ) -> Path:
        context_path = context_path or f"{self.dir_path}/templater.json"
        for file in self.dir_path.rglob("*"):
            if file.is_file() and file.name != "templater.json":
                self.process_output_file(
                    file=file,
                    output_dir=self.output_dir,
                    context_path=context_path,
                )
            if file.is_dir():
                self.process_output_dir(
                    output_dir_path=self.output_dir
                    / file.relative_to(self.dir_path),
                    context_path=context_path,
                )
        return self.output_dir

    def process_output_file(
        self,
        file: Path,
        output_dir: Path,
        context_path: str,
    ) -> None:
        if not self.output_dir:
            self.output_dir = output_dir
        template = Template(file.as_posix())
        template.render(
            save_path=(
                output_dir / file.relative_to(self.dir_path)
            ).as_posix(),
            context_path=context_path,
            create_dirs=True,
        )

    def process_output_dir(
        self,
        output_dir_path: Path,
        context_path: str,
    ) -> None:
        renderer = Renderer(
            template_file_path=output_dir_path,
            save_path=output_dir_path.as_posix(),
            context_path=context_path,
        )
        output_dir_path = renderer.render_file_path(output_dir_path)
        self._create_output_dir(output_dir_path)

    def _create_output_dir(
        self,
        output_dir_path: Path,
    ) -> None:
        output_dir_path.mkdir(parents=True)
