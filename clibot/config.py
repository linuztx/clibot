import json
import os
from typing import Dict, Any

def load_credentials() -> Dict[str, Any]:
    credentials_path = os.path.dirname(os.path.abspath(__file__))
    credentials_file = os.path.join(credentials_path, 'credentials/credentials.json')

    with open(credentials_file, 'r') as f:
        return json.load(f)

credentials = load_credentials()

AI_PROVIDER = os.getenv('AI_PROVIDER', credentials['provider'])
API_KEY = os.getenv('AI_API_KEY', credentials['api_key'])
AI_MODEL = os.getenv('AI_MODEL', credentials['ai_model'])
GROQ_AI_ENDPOINT = os.getenv('AI_ENDPOINT', "https://api.groq.com/openai/v1")
MISTRAL_AI_ENDPOINT = os.getenv('MISTRAL_ENDPOINT', "https://api.mistral.ai/v1")
OLLAMA_AI_ENDPOINT = os.getenv('OLLAMA_ENDPOINT', "http://localhost:11434/v1")
TEMPERATURE = float(os.getenv('TEMPERATURE', credentials['temperature']))
TOP_P = float(os.getenv('TOP_P', credentials['top_p']))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', credentials['max_tokens']))

AI_ENDPOINTS = {
    "groq": GROQ_AI_ENDPOINT,
    "openai": None,
    "mistral": MISTRAL_AI_ENDPOINT,
    "ollama": OLLAMA_AI_ENDPOINT
}