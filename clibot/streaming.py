import time

def streaming_response(text: str, chunk_size: int = 10, delay: float = 0.05):
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        print(chunk, end='', flush=True)
        time.sleep(delay)
    print()
