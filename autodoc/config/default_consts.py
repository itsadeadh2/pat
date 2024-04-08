import os

DEFAULT_ASSISTANT_INSTRUCTIONS = "You are a python docstring generator. Write comprehensible python docstrings for the functions or classes that are given.Return only THE DOCSTRINGS and do not repeat the whole implementation. Do not include 'python' at the start. Do not exceed 120 characters per line."
DEFAULT_PROMPT = "Generate a docstring for the following code: {code}"
DEFAULT_CONFIG_PATH = os.path.expanduser("~") + "/.env.autodoc"
