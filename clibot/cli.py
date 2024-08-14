from clibot.streaming import *
from clibot.system import *
from clibot.colors import *

import requests
import time
import json
import sys
import os


# Help arguments
help_arguments = f"""Usage: clibot [OPTION]... [MESSAGE]
Interact with Clibot via command line.

Options:        
 {LIGHT_CYAN}--setup{COLOR_RESET}      Setup configuration file
 {LIGHT_CYAN}--clear{COLOR_RESET}      Clear conversation history
 {LIGHT_CYAN}--config{COLOR_RESET}     Show configuration settings
 {LIGHT_CYAN}--history{COLOR_RESET}    Show conversation history
 {LIGHT_CYAN}--chat{COLOR_RESET}       Interact in chat mode
 {LIGHT_CYAN}--help{COLOR_RESET}       Help about any options

Examples:
 {LIGHT_GREEN}clibot --setup{COLOR_RESET}
 {LIGHT_GREEN}clibot 'How is my storage usage?'{COLOR_RESET}

Donations:  {LIGHT_YELLOW}https://ko-fi.com/linuztx{COLOR_RESET}
Repository: {LIGHT_YELLOW}https://github.com/linuztx/clibot{COLOR_RESET}"""


providers = f"""Choose Your AI Provider:
1.) Groq    (Free)
2.) OpenAI  (Paid)
3.) Mistral (Paid)
4.) Ollama  (Free)
"""


# Assuming memory directory is within the package directory
package_dir = os.path.dirname(os.path.abspath(__file__))
files_dir = os.path.join(package_dir, 'memory')
if not os.path.exists(files_dir):
    os.makedirs(files_dir)


# Credentials
credentials_name = 'credentials.json'
credentials_dir = 'credentials'
credentials_path = os.path.join(package_dir, credentials_dir)
if not os.path.exists(credentials_path):
    os.makedirs(credentials_path)


# History files
clibot_history_file = os.path.join(files_dir, 'clibot_memory.json')
agent_history_file = os.path.join(files_dir, 'agent_memory.json')


# Get models
def get_models(url, api_key):
    """Get AI models from the provider"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        return response.json()["data"]
    except Exception as e:
        print(f"{LIGHT_RED}Error:{COLOR_RESET} {e}")
        exit()


# Save the credentials
def save_credentials(provider, api_key, ai_model, temperature, top_p, max_tokens):
    with open(f"{credentials_path}/{credentials_name}", 'w') as f:
        json.dump({
                "provider": provider,
                "api_key": api_key, 
                "ai_model": ai_model, 
                "temperature": float(temperature), 
                "top_p": float(top_p), 
                "max_tokens": int(max_tokens),
                }, f)


# Setup clibot
def setup():
    """
    Setup clibot by selecting an AI provider and configuring the AI model.

    This function prompts the user to choose an AI provider and configure the AI model.
    It supports multiple AI providers such as Groq, OpenAI, Mistral, Ollama, and OpenRouter.
    The user is asked to enter the necessary API keys, AI model, and configuration settings.
    The chosen settings are then saved and a setup completion message is displayed.
    """
    print(providers)
    try:
        # Get the chosen AI provider
        provider = input(f"Enter the number of your chosen AI provider:{COLOR_RESET} ")

        # Handle different AI providers
        if provider == '1':
            # Groq provider
            api_key = input(f"Enter your Groq API key (https://console.groq.com/keys):{COLOR_RESET} ").strip()
            print()

            # Get available models from Groq
            models = get_models("https://api.groq.com/openai/v1/models", api_key)

            # Display available models
            for detail in models:
                print(f"{LIGHT_BLUE}Model:{COLOR_RESET} {detail['id']}{COLOR_RESET}  {LIGHT_YELLOW}Context Window:{COLOR_RESET} {detail['context_window']}")
                time.sleep(0.1)

            # Display model documentation
            print()
            print(f"Models Documentation:{COLOR_RESET} {LIGHT_CYAN}https://console.groq.com/docs/models{COLOR_RESET}")
            print(f"Reference Documentation:{COLOR_RESET} {LIGHT_CYAN}https://console.groq.com/docs/api-reference{COLOR_RESET}\n")

            # Get the chosen AI model
            ai_model = input(f"Enter the AI model you want to use (recommended: llama-3.1-70b-versatile):{COLOR_RESET} ").strip() or "llama-3.1-70b-versatile"

            # Get configuration settings
            max_tokens = input(f"Enter your desired maximum output tokens for the AI model (default: 4096):{COLOR_RESET} ").strip() or 4096
            temperature = input(f"Enter your desired temperature (default: 0.5):{COLOR_RESET} ").strip() or 0.5
            top_p = input(f"Enter your desired top_p (default: 0.9):{COLOR_RESET} ").strip() or 0.9

            # Save configuration settings
            save_credentials("groq", api_key, ai_model, temperature, top_p, max_tokens)

            # Display setup completion message
            print(f"\n{LIGHT_GREEN}Setup complete!{COLOR_RESET}🎉\n")
            exit()

        elif provider == '2':
            # OpenAI provider
            api_key = input(f"Enter your OpenAI API key (https://platform.openai.com/settings/profile/api-keys):{COLOR_RESET} ").strip()
            print()

            # Get available models from OpenAI
            models = get_models("https://api.openai.com/v1/models", api_key)

            # Display available models
            for detail in models:
                print(f"{LIGHT_BLUE}Model:{COLOR_RESET} {detail['id']}{COLOR_RESET}")
                time.sleep(0.1)

            # Display model documentation
            print()
            print(f"Models Documentation:{COLOR_RESET} {LIGHT_CYAN}https://platform.openai.com/docs/models/overview{COLOR_RESET}")
            print(f"Reference Documentation:{COLOR_RESET} {LIGHT_CYAN}https://platform.openai.com/docs/api-reference/introduction{COLOR_RESET}\n")

            # Get the chosen AI model
            ai_model = input(f"Enter the AI model you want to use (recommended: gpt-4o-mini):{COLOR_RESET} ").strip() or "gpt-4o-mini"

            # Get configuration settings
            max_tokens = input(f"Enter your desired maximum output tokens for the AI model (default: 4096):{COLOR_RESET} ").strip() or 4096
            temperature = input(f"Enter your desired temperature (default: 0.5):{COLOR_RESET} ").strip() or 0.5
            top_p = input(f"Enter your desired top_p (default: 0.9):{COLOR_RESET} ").strip() or 0.9

            # Save configuration settings
            save_credentials("openai", api_key, ai_model, temperature, top_p, max_tokens)

            # Display setup completion message
            print(f"\n{LIGHT_GREEN}Setup complete!{COLOR_RESET}🎉\n")
            exit()

        elif provider == '3':
            # Mistral provider
            api_key = input(f"Enter your Mistral API key (https://console.mistral.ai/api-keys/):{COLOR_RESET} ").strip()
            print()

            # Get available models from Mistral
            models = get_models("https://api.mistral.ai/v1/models", api_key)

            # Display available models
            for detail in models:
                print(f"{LIGHT_BLUE}Model:{COLOR_RESET} {detail['id']}{COLOR_RESET} {LIGHT_YELLOW}Context Window:{COLOR_RESET} {detail['max_context_length']}")
                time.sleep(0.1)

            # Display model documentation
            print()
            print(f"Models Documentation:{COLOR_RESET} {LIGHT_CYAN}https://docs.mistral.ai/getting-started/models/{COLOR_RESET}")
            print(f"Reference Documentation:{COLOR_RESET} {LIGHT_CYAN}https://docs.mistral.ai/api/{COLOR_RESET}\n")

            # Get the chosen AI model
            ai_model = input(f"Enter the AI model you want to use (recommended: open-mistral-nemo-2407):{COLOR_RESET} ").strip() or "open-mistral-nemo-2407"

            # Get configuration settings
            max_tokens = input(f"Enter your desired maximum output tokens for the AI model (default: 4096):{COLOR_RESET} ").strip() or 4096
            temperature = input(f"Enter your desired temperature (default: 0.5):{COLOR_RESET} ").strip() or 0.5
            top_p = input(f"Enter your desired top_p (default: 0.9):{COLOR_RESET} ").strip() or 0.9

            # Save configuration settings
            save_credentials("mistral", api_key, ai_model, temperature, top_p, max_tokens)

            # Display setup completion message
            print(f"\n{LIGHT_GREEN}Setup complete!{COLOR_RESET}🎉\n")
            exit()

        elif provider == "4":
            # Ollama provider
            api_key = "None"
            print()

            # Get available models from Ollama
            models = get_models("http://localhost:11434/v1/models", api_key)

            # Display available models
            for detail in models:
                print(f"{LIGHT_BLUE}Model:{COLOR_RESET} {detail['id']}{COLOR_RESET}")
                time.sleep(0.1)

            # Display model documentation
            print()
            print(f"Models Documentation:{COLOR_RESET} {LIGHT_CYAN}https://ollama.com/library{COLOR_RESET}")

            # Get the chosen AI model
            ai_model = input(f"Enter the AI model you want to use (recommended: gemma2:2b):{COLOR_RESET} ").strip() or "gemma2:2b"

            # Get configuration settings
            max_tokens = input(f"Enter your desired maximum output tokens for the AI model (default: 4096):{COLOR_RESET} ").strip() or 4096
            temperature = input(f"Enter your desired temperature (default: 0.5):{COLOR_RESET} ").strip() or 0.5
            top_p = input(f"Enter your desired top_p (default: 0.9):{COLOR_RESET} ").strip() or 0.9

            # Save configuration settings
            save_credentials("ollama", api_key, ai_model, temperature, top_p, max_tokens)

            # Display setup completion message
            print(f"\n{LIGHT_GREEN}Setup complete!{COLOR_RESET}🎉\n")
            exit()

        else:
            print(f"{LIGHT_RED}Invalid choice. Please select a valid option.{COLOR_RESET}")
            exit()

    except Exception as e:
        print(f"{LIGHT_RED}An error occurred: {e}{COLOR_RESET}")
        exit()

    except KeyboardInterrupt:
        print(f"\n{LIGHT_RED}Setup cancelled.{COLOR_RESET}")
        exit()


def load_clibot_history():
    if os.path.exists(clibot_history_file):
        try:
            with open(clibot_history_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return [get_system_clibot()]
    else:
        return [get_system_clibot()]


def save_clibot_history(message_history):
    with open(clibot_history_file, "w") as f:
        json.dump(message_history, f, indent=4)


# Check if credentials file exists
if not os.path.exists(f"{credentials_path}/{credentials_name}"):
    setup()


# Clear chat history
def clear_chat_history():
    with open(clibot_history_file, 'w') as f:
        json.dump([get_system_clibot()], f)
    streaming_response('Conversation history cleared. \n')


# Parse command line arguments
def main():
    # Default values
    query = ""

    # Process command line arguments
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == '--help':
            print(help_arguments)
            exit()
        elif args[0] == '--clear':
            clear_chat_history()
            exit()
        elif args[0] == '--setup':
            setup()
        elif args[0] == '--config':
            with open(f"{credentials_path}/{credentials_name}", 'r') as f:
                credentials = json.load(f)
                print(f"{LIGHT_GREEN}{json.dumps(credentials, indent=4)}{COLOR_RESET}\n")
            exit()
        elif args[0] == '--chat':
            from clibot.chat import start_chat
            while True:
               start_chat()
        elif args[0] == '--history':
            try:
                with open(clibot_history_file, 'r') as f:
                    conversation = json.load(f)
                    for entry in conversation:
                        role = entry.get('role', 'unknown')
                        content = entry.get('content', '')
                        if role == 'system':
                            print(f"{LIGHT_GREEN}[SYSTEM]{COLOR_RESET}\n{content}\n")
                        elif role == 'user':
                            print(f"{LIGHT_GREEN}[USER]{COLOR_RESET}\n{content}\n")
                        elif role == 'assistant':
                            print(f"{LIGHT_GREEN}[CLIBOT]{COLOR_RESET}\n{content}\n")
                        else:
                            print(f"{LIGHT_GREEN}[UNKNOWN ROLE]{COLOR_RESET}\n{content}\n")
                        time.sleep(0.1)
            except FileNotFoundError:
                print(f"{LIGHT_RED}No conversation history found.{COLOR_RESET}\n")
                exit()
        elif args[0].startswith('-'):
            print(f'Error: Unknown option "{args[0]}" for "clibot".')
            exit()
        else:
            query = ' '.join(args)

    if not sys.stdin.isatty():
        try:
            stdin_input = sys.stdin.read().strip()
            if stdin_input:
                if query:
                    query = f"#User Prompt: {query}\n\n{stdin_input}".strip()
                else:
                    query = stdin_input
        except EOFError:
            pass  # Handle EOFError gracefully
    
    if query:
        from clibot.config import API_KEY, AI_PROVIDER, GROQ_AI_ENDPOINT, MISTRAL_AI_ENDPOINT, OLLAMA_AI_ENDPOINT
        from openai import AsyncOpenAI
        from clibot.chat import chatbot
        import asyncio
        messages_clibot_history = load_clibot_history()
        arguments = [{"role": "user", "content": query.strip()}]
        try:
            if AI_PROVIDER == "groq":
                    client = AsyncOpenAI(api_key=API_KEY, base_url=GROQ_AI_ENDPOINT)
                    asyncio.run(chatbot(arguments[0], messages_clibot_history, client))
            elif AI_PROVIDER == "openai":
                    client = AsyncOpenAI(api_key=API_KEY)
                    asyncio.run(chatbot(arguments[0], messages_clibot_history, client))
            elif AI_PROVIDER == "mistral":
                    client = AsyncOpenAI(api_key=API_KEY, base_url=MISTRAL_AI_ENDPOINT)
                    asyncio.run(chatbot(arguments[0], messages_clibot_history, client))
            elif AI_PROVIDER == "ollama":
                    client = AsyncOpenAI(api_key=API_KEY, base_url=OLLAMA_AI_ENDPOINT)
                    asyncio.run(chatbot(arguments[0], messages_clibot_history, client))
        except KeyboardInterrupt:
            streaming_response("\nExiting...")
            exit()
    else:
        print(help_arguments)
        exit()