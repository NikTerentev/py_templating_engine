from pathlib import Path
import json
import re
from src import exceptions
from typing import Any

from src.lexer import Lexer
from src import token
from src.parser import Parser
from src import ast


class Renderer:

    def __init__(
        self,
        template_file_path: Path,
        context_path: str = "templater.json",
        save_path: str = "",
        create_dirs: bool = False,
    ) -> None:
        self.template_file_path: Path = template_file_path
        self.context_path: Path = self._validate_context_path(Path(context_path))
        self.create_dirs = create_dirs
        self.context = self.load_context()
        self.save_path: Path | None = (
            self._validate_save_path(
                self.render_file_path(Path(save_path))
            ) if save_path else None
        )

    def _validate_context_path(self, file_path: Path) -> Path:
        if not file_path.is_file():
            raise exceptions.ContextFileNotFoundError(file_path.name)
        if file_path.stat().st_size == 0:
            raise exceptions.ContextFileIsEmpty(file_path.name)
        return file_path

    def _validate_save_path(
        self,
        save_path: Path,
    ) -> Path:
        if not save_path.parent.exists():
            if self.create_dirs:
                save_path.parent.mkdir(parents=True)
            else:
                raise exceptions.SavePathError(save_path.parent.as_posix())
        return save_path

    def render(self) -> None | str:
        lexer = Lexer(self.template_file_path.as_posix())
        lexer.lexical_analysis()
        parser = Parser(lexer.token_list)
        root_node: ast.ExpressionNode = parser.parse_code()
        self.save_path = self.render_file_path(self.save_path)
        rendered_string: None | str = self._render_ast_tree(root_node)

        if not self.save_path:
            return rendered_string

    def render_file_path(
        self,
        file_path: Path,
    ) -> Path:
        match = re.search(
            r"{{(\S*?)(templater\.\S*?)}}",
            file_path.as_posix(),
        )
        if match:
            context_variable = self._get_context_variable(match.groups()[1])
            file_path = Path(
                file_path.as_posix().replace(
                    match.group(),
                    context_variable,
                )
            )
        return file_path

    def _render_ast_tree(self, root_node: ast.ExpressionNode) -> None | str:
        if self.save_path:
            rendered_file = open(self.save_path, "w")
        else:
            rendered_string = ""

        for code_string in root_node.code_strings:
            if code_string.variable.type == token.token_types_list["VARIABLE"]:
                # TODO: Add check for wrong context variables
                code_string.variable.text = self._get_context_variable(
                    code_string.variable.text
                )

            if self.save_path:
                rendered_file.write(code_string.variable.text)
            else:
                rendered_string += code_string.variable.text

        if self.save_path:
            rendered_file.close()
        else:
            return rendered_string

    def _get_context_variable(self, variable: str) -> Any:
        return self.context.get(variable.replace("templater.", "", 1))

    def load_context(self) -> dict[str, str | int | float | bool]:
        with open(self.context_path, "r") as context_file:
            return json.load(context_file)
