import os.path
import logging
from dotenv import load_dotenv
from .default_consts import DEFAULT_CONFIG_PATH, DEFAULT_PROMPT, DEFAULT_ASSISTANT_INSTRUCTIONS


class Config:
    settings = {}

    def __init__(self, config_path=None):
        if not config_path:
            self.__config_path = DEFAULT_CONFIG_PATH

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

    def persist_settings(self):
        env_contents = ""
        for key in self.settings.keys():
            env_contents += f'{key}="{self.settings[key]}"\n'
        with open(self.__config_path, 'wb') as f:
            f.write(env_contents.encode())
        logging.info(f'Settings saved at {self.__config_path}')
        load_dotenv(dotenv_path=self.__config_path)

    def load(self):
        load_dotenv(dotenv_path=DEFAULT_CONFIG_PATH)
        self.settings['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        self.settings['ASSISTANT_ID'] = os.getenv('ASSISTANT_ID')
        self.settings['ASSISTANT_INSTRUCTIONS'] = os.getenv('ASSISTANT_INSTRUCTIONS')
        self.settings['AI_PROMPT'] = os.getenv('AI_PROMPT')