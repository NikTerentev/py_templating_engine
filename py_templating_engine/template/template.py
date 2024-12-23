from pathlib import Path

from py_templating_engine import exceptions
from py_templating_engine.renderer import Renderer


class Template:
    def __init__(self, template_file_path: str) -> None:
        self.template_file_path: Path = self._validate_path(
            Path(template_file_path),
        )

    def _validate_path(self, template_file_path: Path) -> Path:
        if not template_file_path.is_file():
            raise exceptions.TemplateFileNotFoundError(template_file_path.name)
        if template_file_path.stat().st_size == 0:
            raise exceptions.TemplateFileIsEmpty(template_file_path.name)
        return template_file_path

    def render(
        self,
        context_path: str,
        save_path: None | str = None,
        create_dirs: bool = True,
    ) -> None | str:
        renderer = Renderer(
            self.template_file_path,
            context_path,
            save_path,
            create_dirs,
        )

        result: None | str = renderer.render()

        if not save_path:
            return result
        return None
