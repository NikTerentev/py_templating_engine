from templating_engine.lexer import Lexer


def main():
    lexer = Lexer("test_files/first_template.html")
    lexer.lexical_analysis()
    tokens = [
        token for token in lexer.token_list if token.type.name not in [
            "SPACE",
            "CODE",
        ]
    ]

    for token in tokens:
        print(f"Token type: {token.type.name} - value: {token.text} position: {token.position}")


if __name__ == "__main__":
    main()
