from py_templating_engine.environment import TemplatesEnvironment


def main() -> None:
    environment = TemplatesEnvironment("test_files/")
    result = environment.render_project(
        output_dir="created_project",
        create_dirs=True,
    )
    print(result)

    # template: Template = environment.get_template("first_template.html")
    # template.render(
    #     save_path="rendered_files/first_template.html",
    #     context_path="templater.json",
    #     create_dirs=True,
    # )
    # print(rendered_template)


if __name__ == "__main__":
    main()
