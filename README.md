# PAT (Python Auto-documentation Tool)

PAT is a command-line interface tool designed to automatically add docstrings to Python files. It leverages an AI-powered documentation service to generate meaningful docstrings based on the code's context and structure. This tool supports both single Python files and entire directories, allowing for flexible and efficient documentation workflows.

## Disclaimer
**User Responsibility**: The Python Auto-documentation Tool (PAT) utilizes OpenAI's Assistants to analyze and generate docstrings for your Python code. Users must understand that this process involves sending your code to OpenAI's servers for analysis. By using PAT, you agree to this procedure and understand the implications of sending your code to a third-party service.

**Data Security and Privacy**: While OpenAI strives to maintain high standards of data security and privacy, as the developer of PAT, I do not have control over the data once it is in OpenAI's possession. Users are responsible for ensuring that the code they choose to send does not contain sensitive information, proprietary code, or any data that should not be shared with third parties.

**No Liability**: I, the developer of PAT, shall not be held liable for any direct, indirect, incidental, special, consequential or exemplary damages, including but not limited to, damages for loss of profits, goodwill, use, data or other intangible losses (even if I have been advised of the possibility of such damages), resulting from the use of PAT or any data sent to OpenAI's Assistants through the use of this tool.

**Consent and Acknowledgment**: By using PAT, you acknowledge that you have read this disclaimer and understand the responsibilities and risks associated with using this tool. You also consent to the transmission of your code to OpenAI for the purpose of generating docstrings, in accordance with OpenAI's [terms of service](https://openai.com/policies/terms-of-use) and [privacy policies](https://openai.com/policies/privacy-policy).

**Final Decision**: The decision to use PAT and send code to OpenAI's Assistants for analysis rests entirely with the user. Users are advised to review their code for sensitive information and consider the necessity and benefits of using this tool against potential risks to data privacy and security.

## How does this work?
PAT makes use of [OpenAi's Assistants](https://platform.openai.com/docs/assistants/overview) to analyse your code block and generate comprehensive docstrings for it.  
Even though assistants allow you to upload the code to be used as a reference, this tool doesn't do that. Instead it just send your codeblock as a block of text to be analysed by the assistant.
PAT will create a default assistant in your OPENAI account if you don't have one, and properly configure it after the first usage.  
You'll be able to see it using [this link](https://platform.openai.com/playground/assistants).

## How does it look like?
This project itself used the pat library to generate its own documentation, so you can just take a look at the [autodoc folder](autodoc) and see for yourself.

## Installation

Before using AutoDoc CLI, ensure that Python and `pip` are installed on your system. Then, install the tool using the following command:
```bash
pip install git+https://github.com/itsadeadh2/pat.git
```

## Configuration

Before running the AutoDoc CLI for the first time, you must configure it with your OpenAI API key and other optional settings. To configure the tool, run:

```bash
pat configure
```

This will initialize the configuration process, where you'll be prompted to enter your OpenAI API key and other relevant information.  
These settings will be saved for future use in `~/.env.autodoc`

## Usage

AutoDoc CLI offers two modes of operation: processing a single file or an entire folder. Here's how to use each mode:

### Folder Mode

To automatically add docstrings to all Python files in a folder, use:
```bash
pat run --mode folder <PROJECT_FOLDER_PATH>
```

### File Mode

To add docstrings to a single Python file, use:
```bash
pat run --mode file <FILE_PATH>
```
### Formatting

If you wish to format the files after adding the docstrings, add the `--format` flag at the end of the command:
```bash
pat run --mode <mode> <path> --format
```
*This will format your files using the [black library](https://pypi.org/project/black/). If you don't use that it is very likely that the docstrings are not going to be
properly indented.*

## Additional Options

- `--mode, -m` (default: `folder`): Specify the operation mode (`folder` or `file`).
- `--format`: Enable formatting of the file(s) after adding docstrings.

## Support

For support, please open an issue on the GitHub repository page. We welcome contributions and feedback to improve AutoDoc CLI.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.