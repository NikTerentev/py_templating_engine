from src.lexer import Lexer
from src.parser import Parser


def main():
    lexer = Lexer("test_files/first_template.html")
    lexer.lexical_analysis()
    parser = Parser(lexer.token_list)

    root_node = parser.parse_code()

    parser.render(root_node, "first_template.html")


if __name__ == "__main__":
    main()
