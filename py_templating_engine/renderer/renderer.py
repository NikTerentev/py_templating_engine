import json
import re
from pathlib import Path
from typing import Any

from py_templating_engine import ast, exceptions, token
from py_templating_engine.lexer import Lexer
from py_templating_engine.parser import Parser


class Renderer:
    def __init__(
        self,
        template_file_path: Path,
        context_path: str,
        save_path: str = "",
        create_dirs: bool = False,
    ) -> None:
        self.template_file_path: Path = template_file_path
        self.context_path: Path = self._validate_context_path(
            Path(context_path),
        )
        self.create_dirs = create_dirs
        self.context = self.load_context(self.context_path)
        self.save_path: Path | None = (
            self._validate_save_path(self.render_file_path(Path(save_path)))
            if save_path
            else None
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
        lexer = Lexer(self.template_file_path)
        lexer.lexical_analysis()
        parser = Parser(lexer.token_list)
        root_node: ast.ExpressionNode = parser.parse_code()
        self.save_path = self.render_file_path(self.save_path)
        rendered_string: None | str = self._render_ast_tree(root_node)

        if not self.save_path:
            return rendered_string
        return None

    def render_file_path(
        self,
        file_path: Path,
    ) -> Path:
        match = re.search(
            r"{{(\S*?)(templater\.\S*?)}}",
            file_path.as_posix(),
        )
        if match:
            context_variable = self.get_variable_from_context(
                match.groups()[1],
            )
            file_path = Path(
                file_path.as_posix().replace(
                    match.group(),
                    context_variable,
                ),
            )
        return file_path

    def _render_ast_tree(self, root_node: ast.ExpressionNode) -> None | str:
        if self.save_path:
            rendered_file = open(self.save_path, "w")
        else:
            rendered_string = ""

        for code_string in root_node.code_strings:
            if code_string.variable.type == token.token_types_list["VARIABLE"]:
                code_string.variable.text = self.get_variable_from_context(
                    code_string.variable.text,
                )
            if self.save_path:
                rendered_file.write(code_string.variable.text)
            else:
                rendered_string += code_string.variable.text

        if self.save_path:
            rendered_file.close()
        else:
            return rendered_string

    def get_variable_from_context(self, variable: str):
        json_variable = self._get_context_variable(variable)
        if isinstance(json_variable, list):
            return str(json_variable[0])
        if isinstance(json_variable, int | float | bool | str):
            return str(json_variable)
        raise exceptions.CorrectTemplateVariableNotFoundError(
            variable,
            json_variable,
        )

    def _get_context_variable(self, variable: str) -> Any:
        return self.context.get(variable.replace("templater.", "", 1))

    @classmethod
    def load_context(cls, context_path: Path):
        with context_path.open() as context_file:
            return json.load(context_file)
