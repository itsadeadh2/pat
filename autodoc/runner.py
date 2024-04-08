from autodoc.services import AIAutodocService
import os
import ast
import black
import io


class Runner:
    def __init__(self, autodoc_service: AIAutodocService, auto_format: bool):
        self.autodoc_service = autodoc_service
        self.auto_format = auto_format

    def run_for_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.py'):
                    self.process_file(os.path.join(root, file))

    def run_for_file(self, file_path):
        if file_path.endswith('.py'):
            self.process_file(file_path=file_path)

    def add_docstring(self, file: io.TextIOWrapper):
        tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    # Generate a docstring for this node
                    docstring = self.autodoc_service.generate_docstring(node=ast.unparse(node))
                    # Here, you would insert the docstring into the file.
                    if docstring:
                        node.body.insert(0, ast.Expr(ast.Str(docstring)))
                        file.seek(0)
                        file.write(ast.unparse(tree))
                        print(f"Generated docstring for {node.name}: {docstring}")
        file.truncate()
        return file

    def format_file(self, file: io.TextIOWrapper):
        # Autoformat the file using black
        file.seek(0)
        contents = file.read()
        format_mode = black.Mode(
            target_versions={black.TargetVersion.PY310},
            line_length=120,
            string_normalization=True
        )
        formatted_code = black.format_file_contents(src_contents=contents, fast=False, mode=format_mode)
        file.seek(0)
        file.write(formatted_code)
        file.truncate()
        return file

    def process_file(self, file_path):
        with open(file_path, 'r+') as file:
            file = self.add_docstring(file=file)
            if self.auto_format:
                self.format_file(file=file)
