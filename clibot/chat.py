import os
import json
import asyncio
from clibot.animation import LoadingAnimation
from clibot.system import get_system_clibot
from clibot.streaming import streaming_response
from clibot.config import *
from clibot.colors import *
from openai import AsyncOpenAI


package_dir = os.path.dirname(os.path.abspath(__file__))
files_dir = os.path.join(package_dir, 'memory')
history_file = os.path.join(files_dir, 'clibot_memory.json')


help_msg = f"""Available Commands:
 /help    Show this help message
 /bye     Exit the chat
 /clear   Clear the conversation history"""


def load_chat_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return [get_system_clibot()]
    else:
        return [get_system_clibot()]


def save_chat_history(message_history):
        with open(history_file, "w") as f:
                json.dump(message_history, f, indent=4)


def clear_chat_history():
        with open(history_file, 'w') as f:
                json.dump([get_system_clibot()], f)
        streaming_response('Conversation history cleared. \n')


async def chatbot(messages, messages_history, client):
    system_prompt = get_system_clibot()
    if messages_history:
        messages_history[0] = system_prompt
    else:
        messages_history.append(system_prompt)

    messages_history.append(messages)

    loading = LoadingAnimation()
    
    try:
        loading.start()
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=messages_history,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,
            stream=True,
            # stop=None
        )
        loading.stop()
        respond = ""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                respond += content
        print()
        messages_history.append({"role": "assistant", "content": respond})
        save_chat_history(messages_history)
        print()

    except KeyboardInterrupt:
         loading.stop()
         streaming_response(f"\n{LIGHT_RED}Exiting...{COLOR_RESET}")
         exit()

    except Exception as e:
        loading.stop()
        streaming_response(f"{LIGHT_RED}Error: {str(e)}{COLOR_RESET}\n")
        exit()

    except RuntimeError:
        pass


def start_chat():
        try:
            query = input(">>> ").strip() or "/help"
            if query == "/bye":
                    exit()
            elif query == "/help":
                    print(help_msg + "\n")
            elif query == "/clear":
                    clear_chat_history()
            else:
                if AI_PROVIDER == "groq":
                        client = AsyncOpenAI(api_key=API_KEY, base_url=GROQ_AI_ENDPOINT)
                elif AI_PROVIDER == "openai":
                        client = AsyncOpenAI(api_key=API_KEY)
                elif AI_PROVIDER == "mistral":
                        client = AsyncOpenAI(api_key=API_KEY, base_url=MISTRAL_AI_ENDPOINT)
                elif AI_PROVIDER == "ollama":
                        client = AsyncOpenAI(api_key=API_KEY, base_url=OLLAMA_AI_ENDPOINT)
                asyncio.run(chatbot({"role": "user", "content": query}, load_chat_history(), client))
        except KeyboardInterrupt:
                print("\nExiting...")
                exit()
        except Exception as e:
                print(f"\n{LIGHT_RED}Error: {str(e)}{COLOR_RESET}")
                exit()
        except RuntimeError:
                pass

