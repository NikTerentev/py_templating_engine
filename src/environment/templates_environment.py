from pathlib import Path
from src import exceptions
from src.template import Template


class TemplatesEnvironment:

    def __init__(self, dir_path: str) -> None:
        self.dir_path: Path = self._validate_path(Path(dir_path))

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
        # TODO: Add default value for output_dir
        output_dir: str,
        create_dirs: bool = True,
        context_path: str = "templater.json",
    ) -> str:
        self._process_output_dir(Path(output_dir), create_dirs)
        for file in self.dir_path.rglob("*"):
            if file.is_file():
                template = Template(file.as_posix())
                template.render(
                    save_path=(
                        Path(output_dir) / file.relative_to(self.dir_path)
                    ).as_posix(),
                    context_path=context_path,
                    create_dirs=True,
                )
            elif file.is_dir():
                self._process_output_dir(
                    output_dir / file.relative_to(self.dir_path),
                    create_dirs,
                )
        return output_dir

    def _process_output_dir(
        self,
        output_dir_path: Path,
        create_dirs: bool,
    ) -> None:
        if not output_dir_path.exists():
            if create_dirs:
                output_dir_path.mkdir(parents=True)
            else:
                raise exceptions.SavePathError(output_dir_path.as_posix())
