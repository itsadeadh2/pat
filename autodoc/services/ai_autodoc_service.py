from openai import OpenAI


class AIAutodocService:
    """
    This class provides a service for automatically generating docstrings using an AI assistant.

    Attributes:
        __client (OpenAI): An instance of the OpenAI API client.
        __assistant_id (str): The unique identifier for the AI assistant used for generating docstrings.
        __prompt (str): A predefined template for the prompt to be sent to the AI assistant.

    Methods:
        __init__(assistant_id: str, assistant_instructions: str, prompt: str): Initializes the AIAutodocService with
            an optional assistant ID, instructions for creating a new assistant if needed, and a prompt template.
        generate_docstring(node: str) -> str: Generates a docstring for the given code node and returns it.
        get_assistant_id() -> str: Returns the unique identifier of the AI assistant being used.
    """

    def __init__(self, assistant_id: str, assistant_instructions: str, prompt: str):
        """Initializes an instance with a specified assistant ID or creates a new assistant if no ID is provided.

        Args:
            assistant_id (str): The unique identifier for an existing assistant. If empty, a new assistant will be created.
            assistant_instructions (str): Instructions for the assistant, used only if creating a new assistant.
            prompt (str): The initial prompt to be used with the assistant.

        Attributes:
            __client (OpenAI): An instance of the OpenAI API client.
            __assistant_id (str): The unique identifier for the assistant, either provided or obtained after creation.
            __prompt (str): The initial prompt saved for future use with the assistant.
        """
        self.__client = OpenAI()
        if assistant_id:
            self.__assistant_id = assistant_id
        else:
            assistant = self.__client.beta.assistants.create(
                name="AutoDoc",
                instructions=assistant_instructions,
                tools=[{"type": "code_interpreter"}],
                model="gpt-4-turbo-preview",
            )
            self.__assistant_id = assistant.id
        self.__prompt = prompt

    def generate_docstring(self, node: str):
        """Generates a docstring for the given code snippet using an API client.

        This method leverages an API client to create a thread, send a prompt containing the code snippet (node),
        and poll the thread for a response. It processes the completed run to extract, clean, and return the generated
        docstring. If the run does not complete, it prints the run status and returns an empty string.

        Parameters:
        - node (str): The code snippet for which the docstring is to be generated.

        Returns:
        - str: The generated docstring for the provided code snippet, or an empty string if the run is not completed.
        """
        thread = self.__client.beta.threads.create()
        prompt = self.__prompt.format(code=node)
        message = self.__client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = self.__client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=self.__assistant_id)
        if run.status == "completed":
            messages = self.__client.beta.threads.messages.list(thread_id=thread.id)
            docstring = messages.data[0].content[0].text.value
            docstring = docstring.replace('"', "")
            docstring = docstring.replace("`", "")
            return docstring
        else:
            print(run.status)
            return ""

    def get_assistant_id(self):
        """Returns the private __assistant_id attribute of the instance."""
        return self.__assistant_id
