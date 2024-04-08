from autodoc.services import AIAutodocService
import os
import ast
import black
import io


class Runner:
    """
    Represents a runner class that automatically generates and inserts docstrings into Python files.

    Attributes:
        autodoc_service (AIAutodocService): The service used to generate docstrings.
        auto_format (bool): Whether to format the files using Black after adding docstrings.

    Methods:
        run_for_folder(folder_path): Processes all Python files (.py) found in a directory tree.
        run_for_file(file_path): Generates and inserts docstrings for a single Python file.
        add_docstring(file): Generates and adds docstrings to missing function, class, and method definitions within a file.
        format_file(file): Formats the given file using black formatter.
        process_file(file_path): Opens a file, calls add_docstring and optionally format_file on it.
    """

    def __init__(self, autodoc_service: AIAutodocService, auto_format: bool):
        """
        Initialize the instance with an AI-based documentation service and an option to auto format the documentation.

        :param autodoc_service: An instance of AIAutodocService to generate the documentation.
        :param auto_format: A boolean indicating whether the documentation should be auto-formatted.
        """
        self.autodoc_service = autodoc_service
        self.auto_format = auto_format

    def run_for_folder(self, folder_path):
        """Iterates through all files in a given folder (and its subfolders), and processes each Python file found.

        Args:
            folder_path (str): The path to the folder where the search should begin.

        This method relies on the process_file method to handle the processing of each Python file found.
        """
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    self.process_file(os.path.join(root, file))

    def run_for_file(self, file_path):
        """
        Executes processing on a file if it has a .py extension.

        Args:
            file_path (str): The path of the file to be processed.

        This method checks if the given file path ends with the '.py' extension, indicating a Python file.
        If the condition is satisfied, it calls the process_file method, passing the file path as an argument.
        """
        if file_path.endswith(".py"):
            self.process_file(file_path=file_path)

    def add_docstring(self, file: io.TextIOWrapper):
        """
        Automatically generates and inserts missing docstrings for functions, asynchronous functions, and classes within
        a Python file using an auto-documentation service.

        Parameters:
            file (io.TextIOWrapper): An open file object for reading and writing, typically from built-in open() function.

        Returns:
            io.TextIOWrapper: The modified file object with inserted docstrings for any functions, asynchronous functions,
                               and classes that previously lacked them.
        """
        tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    docstring = self.autodoc_service.generate_docstring(node=ast.unparse(node))
                    if docstring:
                        node.body.insert(0, ast.Expr(ast.Str(docstring)))
                        file.seek(0)
                        file.write(ast.unparse(tree))
                        print(f"Generated docstring for {node.name}: {docstring}")
        file.truncate()
        return file

    def format_file(self, file: io.TextIOWrapper):
        """
        Formats the contents of a given file using the Black code formatter with specific configurations.

        Args:
            file (io.TextIOWrapper): The file to format. The file must be open for reading and writing.

        Returns:
            io.TextIOWrapper: The same file object with its contents formatted according to the specified Black mode.

        Note:
            This function specifically targets Python 3.10, sets the maximum line length to 120 characters,
            and enables string normalization. It does not use 'fast' mode for formatting.
        """
        file.seek(0)
        contents = file.read()
        format_mode = black.Mode(
            target_versions={black.TargetVersion.PY310}, line_length=120, string_normalization=True
        )
        formatted_code = black.format_file_contents(src_contents=contents, fast=False, mode=format_mode)
        file.seek(0)
        file.write(formatted_code)
        file.truncate()
        return file

    def process_file(self, file_path):
        """
        Processes a given file by adding a docstring and optionally formatting it based on the auto_format attribute.

        Args:
            file_path (str): The path to the file to be processed.

        The file at the given file_path is opened in read+write mode, a docstring is added using the add_docstring method,
        and if the auto_format attribute is True, the file is also formatted using the format_file method.
        """
        with open(file_path, "r+") as file:
            file = self.add_docstring(file=file)
            if self.auto_format:
                self.format_file(file=file)
