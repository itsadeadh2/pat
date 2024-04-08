from openai import OpenAI


class AIAutodocService:
    def __init__(self, assistant_id: str, assistant_instructions: str, prompt: str):
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
        thread = self.__client.beta.threads.create()
        prompt = self.__prompt.format(code=node)
        message = self.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        run = self.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=self.__assistant_id
        )
        if run.status == 'completed':
            messages = self.__client.beta.threads.messages.list(
                thread_id=thread.id
            )
            docstring = messages.data[0].content[0].text.value
            docstring = docstring.replace('"', '')
            docstring = docstring.replace('`', '')
            return docstring
        else:
            print(run.status)
            return ''

    def get_assistant_id(self):
        return self.__assistant_id
