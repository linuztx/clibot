# Clibot

Clibot is an innovative command-line productivity tool powered by advanced language models. It helps you accomplish tasks faster and more efficiently by interacting with AI models directly from the command line. Clibot supports various command line interfaces including CMD, PowerShell, Zsh, and more.

![clibot](https://github.com/user-attachments/assets/495ef66d-e494-4bc5-a464-46bf7d3d6782)

## Installation

To install Clibot, run the following command:

```bash
pip install clibot
```

> [!TIP]
> You can use locally hosted open source models which are available for free. To use local models, you will need to run your own LLM backend server such as [Ollama](https://github.com/ollama/ollama).
>
> **❗️Note: Localhosted models require high-end hardware for optimal performance and may not work as expected on lower-end systems.**

### Features

- **Multi-Provider Support**: Compatible with multiple AI providers including Groq, OpenAI, Mistral, and Ollama.
- **Conversation History**: Keeps track of your conversations for easy review.
- **Setup and Configuration**: Streamlined setup process to configure your AI providers.

### Setup

After installation, run the following command to set up Clibot:

```bash
clibot
```

### Usage

Use Clibot by executing the `clibot` command followed by your query or command. Here are some examples:

- General Queries:

```bash
clibot "How is my system?"
```

- Summarizing multiple files:

```bash
clibot "Summarize" < file1.txt < file2.txt
```

- Creating and saving files:

```bash
clibot 'Write a simple README file' > README.md
```

- Reviewing CPU information:

```bash
lscpu | clibot 'Review my CPU'
```

Feel free to explore the various capabilities of Clibot and make the most out of this powerful command-line productivity tool!

### Donations

If you find this project useful, consider supporting my work by making a donation. Every contribution helps me continue developing and maintaining this project.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/linuztx)
