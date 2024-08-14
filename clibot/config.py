import json
import os

credentials_path = os.path.dirname(os.path.abspath(__file__))
credentials_file = os.path.join(credentials_path, 'credentials/credentials.json')

with open(credentials_file, 'r') as f:
    credentials = json.load(f)

AI_PROVIDER = os.getenv('AI_PROVIDER', credentials['provider'])

# GROQ API KEY
API_KEY=os.getenv('AI_API_KEY', credentials['api_key'])

# GROQ AI MODEL
AI_MODEL=os.getenv('AI_MODEL', credentials['ai_model'])

# GROQ AI ENDPOINT
GROQ_AI_ENDPOINT=os.getenv('AI_ENDPOINT', "https://api.groq.com/openai/v1")

# MISTRAL AI ENDPOINT
MISTRAL_AI_ENDPOINT=os.getenv('MISTRAL_ENDPOINT', "https://api.mistral.ai/v1")

# OLLAMA AI ENDPOINT
OLLAMA_AI_ENDPOINT=os.getenv('OLLAMA_ENDPOINT', "http://localhost:11434/v1")

# TEMPERATURE
TEMPERATURE = os.getenv('TEMPERATURE', credentials['temperature'])

# TOP P
TOP_P = os.getenv('TOP_P', credentials['top_p'])

# MAX TOKENS
MAX_TOKENS = os.getenv('MAX_TOKENS', credentials['max_tokens'])
