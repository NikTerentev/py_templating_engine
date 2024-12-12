class TemplateException(ValueError):
    """Basic class for all templates dir exceptions."""

    error: str

    def __init__(self, error_message: str) -> None:
        super().__init__()
        self.error_message = error_message

    def __str__(self) -> str:
        return f"{self.error_message}"


class TemplatesDirNotFoundError(TemplateException):
    """Exception for case when templates dir not found."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Template directory {path} not found!")


class TemplatesDirIsEmpty(TemplateException):
    """Exception for case when templates dir is empty."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Templates directory {path} is empty!")


class TemplateFileNotFoundError(TemplateException):
    """Exception for case when template file not found."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Template file {path} not found!")


class TemplateFileIsEmpty(TemplateException):
    """Exception for case when template file is empty."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Template file {path} is empty!")


class ContextFileNotFoundError(TemplateException):
    """Exception for case when context file not found."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Context file {path} not found!")


class ContextFileIsEmpty(TemplateException):
    """Exception for case when context file is empty."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Context file {path} is empty!")


class SavePathError(TemplateException):
    """Exception for case when context file is empty."""

    def __init__(self, path: str) -> None:
        """Initialize exception instance."""
        super().__init__(f"Save path {path} doesn't exist!")
