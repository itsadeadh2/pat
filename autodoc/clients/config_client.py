import os.path
import logging
from dotenv import load_dotenv

DEFAULT_ASSISTANT_INSTRUCTIONS = "You are a python docstring generator. Write comprehensible python docstrings for the functions or classes that are given.Return only THE DOCSTRINGS and do not repeat the whole implementation. Do not include 'python' at the start. Do not exceed 120 characters per line."
DEFAULT_PROMPT = "Generate a docstring for the following code: {code}"
DEFAULT_CONFIG_PATH = os.path.expanduser("~") + '/.env.autodoc'


class Config:
    settings = {}

    def initialize(self):
        open_ai_key = input("Please input your OpenAI API Key: ")
        if not open_ai_key:
            logging.info('No open API key specified. Trying to grab from Environment Variables')
            open_ai_key = os.getenv('OPEN_API_KEY')
            if not open_ai_key:
                raise ValueError('You need to provide an OPEN API KEY!')
        assistant_id = input("Please insert your assistant ID (leave it empty to create one): ")
        assistant_instructions = input(
            "Custom assistant instructions command (leave it empty to use the default one): ")
        if not assistant_instructions:
            assistant_instructions = DEFAULT_ASSISTANT_INSTRUCTIONS
        prompt = input("Custom prompt command (leave it empty to use the default one): ")
        if not prompt:
            prompt = DEFAULT_PROMPT

        self.settings['OPENAI_API_KEY'] = open_ai_key
        self.settings['ASSISTANT_ID'] = assistant_id
        self.settings['ASSISTANT_INSTRUCTIONS'] = assistant_instructions
        self.settings['AI_PROMPT'] = prompt
        self.persist_settings()
        logging.info(f'Settings saved at {DEFAULT_CONFIG_PATH}')

    def persist_settings(self):
        env_contents = ""
        for key in self.settings.keys():
            env_contents += f'{key}="{self.settings[key]}"\n'
        with open(DEFAULT_CONFIG_PATH, 'wb') as f:
            f.write(env_contents.encode())
        load_dotenv(dotenv_path=DEFAULT_CONFIG_PATH)

    def load(self):
        load_dotenv(dotenv_path=DEFAULT_CONFIG_PATH)
        self.settings['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        self.settings['ASSISTANT_ID'] = os.getenv('ASSISTANT_ID')
        self.settings['ASSISTANT_INSTRUCTIONS'] = os.getenv('ASSISTANT_INSTRUCTIONS')
        self.settings['AI_PROMPT'] = os.getenv('AI_PROMPT')