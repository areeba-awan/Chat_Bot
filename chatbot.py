# If you get ModuleNotFoundError, run: pip install -r requirements.txt
import os
import chainlit as cl # type: ignore
from dotenv import load_dotenv # type: ignore
import litellm # type: ignore

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Ensure the Gemini API key is set in the environment for LiteLLM
if GEMINI_API_KEY:
    os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
else:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content

    # Call Gemini via LiteLLM with only the current prompt
    try:
        response = litellm.completion(
            model="gemini/gemini-1.5-flash-latest",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_reply = response['choices'][0]['message']['content']
    except Exception as e:
        bot_reply = f"Error: {e}"

    # Display only the latest assistant reply
    await cl.Message(content=bot_reply).send() 