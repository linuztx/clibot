# Clibot

[![PyPI version](https://badge.fury.io/py/clibot.svg)](https://badge.fury.io/py/clibot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/clibot.svg)](https://pypi.org/project/clibot/)

Clibot is an innovative command-line productivity tool powered by advanced language models. It helps you accomplish tasks faster and more efficiently by interacting with AI models directly from the command line. Clibot supports various command line interfaces including CMD, PowerShell, Zsh, and more.

https://github.com/user-attachments/assets/6cb76ad5-3a8d-4bd9-9068-6ec4f99793d0

## Features

- 🌐 **Multi-Provider Support**: Compatible with multiple AI providers including Groq, OpenAI, Mistral, and Ollama.
- 💬 **Conversation History**: Keeps track of your conversations for easy review.
- 🔧 **Setup and Configuration**: Streamlined setup process to configure your AI providers.
- ⚡ **Asynchronous Processing**: Utilizes asynchronous operations for improved performance.
- 🛡️ **Error Handling**: Robust error handling and retry mechanisms for a smooth user experience.
- ⚙️ **Customizable Settings**: Adjust AI model parameters like temperature and max tokens.
- 💾 **File Saving**: Save files directly from Clibot responses.
- 🖥️ **Terminal Command Execution**: Execute terminal commands through Clibot.
- 🐍 **Python Code Execution**: Run Python code snippets within Clibot.

## Installation

Install Clibot using pip:

```bash
pip install clibot
```

> [!TIP]
> You can use locally hosted open source models which are available for free. To use local models, you will need to run your own LLM backend server such as [Ollama](https://github.com/ollama/ollama).
>
> **❗️Note: Locally hosted models require high-end hardware for optimal performance and may not work as expected on lower-end systems.**

## Getting Started

### Setup

After installation, set up Clibot by running:

```bash
clibot
```

Follow the prompts to configure your AI providers and preferences.

### Basic Usage

Use Clibot by executing the `clibot` command followed by your query or command:

```bash
clibot "How is my system?"
```

## Advanced Usage

### Summarizing Multiple Files

```bash
clibot "Summarize" < file1.txt < file2.txt
```

### Creating and Saving Files

```bash
clibot 'Write a simple README file' > README.md
```

### Reviewing System Information

```bash
lscpu | clibot 'Review my CPU'
```

## Upcoming Features: Agentic Capabilities

I'm excited to announce that in upcoming updates, Clibot will be enhanced with agentic capabilities, taking its functionality to the next level:

- 🤖 **Autonomous Task Execution**: Clibot will be able to break down complex tasks into smaller steps and execute them autonomously.
- 🔄 **Adaptive Decision Making**: The AI will make decisions based on the current context and previous interactions, adapting its approach as needed.
- 🔍 **Proactive Information Gathering**: Clibot will actively seek out additional information when necessary to complete tasks more effectively.
- 🎯 **Goal-Oriented Behavior**: Users will be able to set high-level goals, and Clibot will work towards achieving them independently.
- 🧠 **Enhanced Problem Solving**: The AI will utilize its expanded capabilities to tackle more complex problems and provide more comprehensive solutions.

These agentic features will make Clibot an even more powerful assistant, capable of handling a wider range of tasks with increased autonomy and intelligence. Stay tuned for updates!

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/linuztx/clibot/issues) on GitHub.

## Donations

If you find this project useful, consider supporting my work by making a donation. Every contribution helps me continue developing and maintaining this project.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/linuztx)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
