from clibot.streaming import *
from clibot.system import *
from clibot.colors import *
from clibot.chat import chatbot, load_chat_history, start_chat
import asyncio  # Add this import
import requests
import time
import json
import sys
import os
import argparse


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
    """
    print(providers)
    try:
        provider = input(f"Enter the number of your chosen AI provider:{COLOR_RESET} ")
        
        provider_handlers = {
            '1': setup_groq,
            '2': setup_openai,
            '3': setup_mistral,
            '4': setup_ollama
        }
        
        if provider in provider_handlers:
            provider_handlers[provider]()
        else:
            print(f"{LIGHT_RED}Invalid choice. Please select a valid option.{COLOR_RESET}")
            exit()

    except Exception as e:
        print(f"{LIGHT_RED}An error occurred: {e}{COLOR_RESET}")
        exit()
    except KeyboardInterrupt:
        print(f"\n{LIGHT_RED}Setup cancelled.{COLOR_RESET}")
        exit()

def setup_groq():
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

def setup_openai():
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

def setup_mistral():
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

def setup_ollama():
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
async def async_main():
    parser = argparse.ArgumentParser(description="Interact with Clibot via command line.", add_help=False)
    parser.add_argument('--setup', action='store_true', help='Setup configuration file')
    parser.add_argument('--clear', action='store_true', help='Clear conversation history')
    parser.add_argument('--config', action='store_true', help='Show configuration settings')
    parser.add_argument('--history', action='store_true', help='Show conversation history')
    parser.add_argument('--chat', action='store_true', help='Interact in chat mode')
    parser.add_argument('--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('query', nargs='*', help='Query for Clibot')

    args = parser.parse_args()

    if args.help:
        print(help_arguments)
    elif args.clear:
        clear_chat_history()
    elif args.setup:
        setup()
    elif args.config:
        show_config()
    elif args.chat:
        while True:
            await start_chat()
    elif args.history:
        show_history()
    elif args.query or not sys.stdin.isatty():
        await process_query(args)
    else:
        print(help_arguments)

def main():
    asyncio.run(async_main())

def show_config():
    with open(f"{credentials_path}/{credentials_name}", 'r') as f:
        credentials = json.load(f)
        print(f"{LIGHT_GREEN}{json.dumps(credentials, indent=4)}{COLOR_RESET}\n")

def show_history():
    try:
        with open(clibot_history_file, 'r') as f:
            conversation = json.load(f)
            for entry in conversation:
                role = entry.get('role', 'unknown')
                content = entry.get('content', '')
                role_color = {
                    'system': LIGHT_GREEN,
                    'user': LIGHT_CYAN,
                    'assistant': LIGHT_YELLOW
                }.get(role, LIGHT_WHITE)
                print(f"{role_color}[{role.upper()}]{COLOR_RESET}\n{content}\n")
                time.sleep(0.1)
    except FileNotFoundError:
        print(f"{LIGHT_RED}No conversation history found.{COLOR_RESET}\n")

async def process_query_async(query, messages_clibot_history, client):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            arguments = [{"role": "user", "content": query.strip()}]
            await chatbot(arguments[0], messages_clibot_history, client)
            break  # If successful, break out of the retry loop
        except Exception as e:
            if attempt < max_retries - 1:  # If not the last attempt
                print(f"\n{LIGHT_YELLOW}Warning: Error occurred. Retrying... (Attempt {attempt + 1}/{max_retries}){COLOR_RESET}")
                await asyncio.sleep(1)  # Wait a bit before retrying
            else:
                print(f"\n{LIGHT_RED}Error: Failed to process query after {max_retries} attempts. Details: {str(e)}{COLOR_RESET}")
                raise  # Re-raise the last exception if all retries failed

async def process_query(args):
    query = ' '.join(args.query)
    if not sys.stdin.isatty():
        stdin_input = sys.stdin.read().strip()
        if stdin_input:
            query = f"#User Prompt: {query}\n\n{stdin_input}" if query else stdin_input

    if query:
        from clibot.config import API_KEY, AI_PROVIDER, AI_ENDPOINTS
        from openai import AsyncOpenAI

        messages_clibot_history = load_chat_history()
        try:
            client = AsyncOpenAI(
                api_key=API_KEY,
                base_url=AI_ENDPOINTS.get(AI_PROVIDER)
            )
            await process_query_async(query, messages_clibot_history, client)
        except KeyboardInterrupt:
            streaming_response("\nExiting...")
            exit()
        except RuntimeError as e:
            if "Event loop is closed" in str(e):
                print(f"\n{LIGHT_RED}Error: The event loop was closed unexpectedly. Restarting the query...{COLOR_RESET}")
                # Attempt to recreate the event loop and run the query again
                asyncio.set_event_loop(asyncio.new_event_loop())
                try:
                    await process_query_async(query, messages_clibot_history, client)
                except Exception as inner_e:
                    print(f"\n{LIGHT_RED}Error: Unable to process the query. Please try again. Details: {str(inner_e)}{COLOR_RESET}")
            else:
                print(f"\n{LIGHT_RED}Error: An unexpected runtime error occurred. Details: {str(e)}{COLOR_RESET}")
        except Exception as e:
            print(f"\n{LIGHT_RED}Error: An unexpected error occurred. Details: {str(e)}{COLOR_RESET}")

if __name__ == "__main__":
    main()