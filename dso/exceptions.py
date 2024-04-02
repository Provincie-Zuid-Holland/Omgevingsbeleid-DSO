class TemplateError(Exception):
    """Exception raised for errors in the template processing."""

    def __init__(self, template_name: str, message: str = "Error processing template"):
        self.template_name = template_name
        self.message = f"{message}: {template_name}"
        super().__init__(self.message)


class FileWriteError(Exception):
    """Exception raised for errors during file writing."""

    def __init__(self, file_path: str, message: str = "Error writing to file"):
        self.file_path = file_path
        self.message = f"{message}: {file_path}"
        super().__init__(self.message)


class PublicationServiceError(Exception):
    def __init__(self, message: str = "Error building document"):
        super().__init__(message)
