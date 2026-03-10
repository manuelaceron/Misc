""" 
Claude Opus
Claude Sonnet
Claude Haiku

+++ Intelligence
+++ Cost/Speed


1. Tokenization
2. Embedding
3. Cpntextualization: each embedding is adjusted based on other embeddings around it. Give  more sense.
4. Generation

"""

from dotenv import load_dotenv
from anthropic import Anthropic

if __name__ == "__main__":
    
    load_dotenv()
    
    # Use Anthopic SDK (wrapper for HTTP calls)
    client = Anthropic()
    model = "claude-sonnet-4-0"
    max_toakens=1000 #caps lengths of response to this value
    
    message = client.messages.create(
        model=model,
        max_tokens=max_toakens,
        messages=[
            {
                "role": "user",
                "content": "What is quantum computing? Answer in one sentence"    
            }
        ])
    print(message)
    print(message.content[0].text)
    
    #Anthropic and Claude dont store any messages:
    # - To have a context, manually keep a list a messages in the code
    
    
    