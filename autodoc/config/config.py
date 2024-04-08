import os.path
import logging
from dotenv import load_dotenv
from .default_consts import DEFAULT_CONFIG_PATH, DEFAULT_PROMPT, DEFAULT_ASSISTANT_INSTRUCTIONS


class Config:
    """
    A class for managing configuration settings for an application, including OpenAI API key and assistant details.

    Attributes:
        settings (dict): A dictionary to store configuration settings.

    Methods:
        __init__(config_path=None): Initializes the config object. Optionally sets a custom configuration path; otherwise,
                                    uses a default path.
        initialize(): Interactively collects OpenAI API key, assistant ID, assistant instructions, and AI prompt from the
                      user, validates them, and saves them to the configuration settings.
        persist_settings(): Persists the current settings to a file specified by __config_path, allowing them to be
                            reloaded later.
        load(): Loads previously saved settings from a file into the settings dictionary.
    """

    settings = {}

    def __init__(self, config_path=None):
        """
        Initialize the object with a configuration file path.

        :param config_path: Optional; the path to the configuration file. If not provided, a default path is used.
        """
        if not config_path:
            self.__config_path = DEFAULT_CONFIG_PATH

    def initialize(self):
        """Initializes the application with OpenAI API key, assistant ID, assistant instructions, and AI prompt.

        This method prompts the user to enter the OpenAI API key, assistant ID, custom assistant instructions, and a
        custom AI prompt. If the OpenAI API key is not provided, it attempts to retrieve it from environment variables.
        Defaults are used for assistant instructions and AI prompt if not provided by the user. The settings are then
        saved to the application's configuration.
        """
        open_ai_key = input("Please input your OpenAI API Key: ")
        if not open_ai_key:
            logging.info("No open API key specified. Trying to grab from Environment Variables")
            open_ai_key = os.getenv("OPEN_API_KEY")
            if not open_ai_key:
                raise ValueError("You need to provide an OPEN API KEY!")
        assistant_id = input("Please insert your assistant ID (leave it empty to create one): ")
        assistant_instructions = input(
            "Custom assistant instructions command (leave it empty to use the default one): "
        )
        if not assistant_instructions:
            assistant_instructions = DEFAULT_ASSISTANT_INSTRUCTIONS
        prompt = input("Custom prompt command (leave it empty to use the default one): ")
        if not prompt:
            prompt = DEFAULT_PROMPT
        self.settings["OPENAI_API_KEY"] = open_ai_key
        self.settings["ASSISTANT_ID"] = assistant_id
        self.settings["ASSISTANT_INSTRUCTIONS"] = assistant_instructions
        self.settings["AI_PROMPT"] = prompt
        self.persist_settings()

    def persist_settings(self):
        """
        Writes the current settings to a configuration file in .env format, encodes the content in bytes, and logs the file path.
        It also reloads the environment variables from the newly updated configuration file. Assumes 'load_dotenv' is available.
        """
        env_contents = ""
        for key in self.settings.keys():
            env_contents += f'{key}="{self.settings[key]}"\n'
        with open(self.__config_path, "wb") as f:
            f.write(env_contents.encode())
        logging.info(f"Settings saved at {self.__config_path}")
        load_dotenv(dotenv_path=self.__config_path)

    def load(self):
        """
        Loads environment variables from a default config path and sets them into the settings dictionary of the instance.

        This method utilizes the load_dotenv function to load environment variables from a .env file located by the
        DEFAULT_CONFIG_PATH. It then sets various settings including 'OPENAI_API_KEY', 'ASSISTANT_ID',
        'ASSISTANT_INSTRUCTIONS', and 'AI_PROMPT' into the instance's settings dictionary by fetching these variables from the
        system's environment variables using os.getenv.
        """
        load_dotenv(dotenv_path=DEFAULT_CONFIG_PATH)
        self.settings["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.settings["ASSISTANT_ID"] = os.getenv("ASSISTANT_ID")
        self.settings["ASSISTANT_INSTRUCTIONS"] = os.getenv("ASSISTANT_INSTRUCTIONS")
        self.settings["AI_PROMPT"] = os.getenv("AI_PROMPT")
