from pathlib import Path

from py_templating_engine.environment import TemplatesEnvironment


def main() -> None:
    environment = TemplatesEnvironment(Path("test_template"))
    result = environment.render_project()
    print(result)

    # template: Template = environment.get_template("first_template.html")
    # template.render(
    #     save_path="rendered_files/first_template.html",
    #     context_path="test_template/templater.json",
    #     create_dirs=True,
    # )
    # print(rendered_template)


if __name__ == "__main__":
    main()
