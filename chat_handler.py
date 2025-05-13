import openai
from dotenv import load_dotenv
import os
from flask import request, jsonify
import logging

# Set your OpenAI API key (Make sure to replace this with your actual key or set it using environment variables)
load_dotenv(dotenv_path="confidential.env")  # Load environment variables from .env

openai.api_key = os.getenv('openai_api_key')
# Configure logging to show debug messages
logging.basicConfig(level=logging.DEBUG)

# Chat history to keep context
chat_history = [
    {"role": "system", "content": "You are a friendly, conversational car consultant named Chitti who always addresses the user as 'Sir'."}
]

def chat_handler():
    user_input = request.json.get("message", "")
    logging.debug(f"User input received: {user_input}")

    # Add user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    try:
        # Make a request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        bot_reply = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": bot_reply})
        logging.debug(f"Bot response: {bot_reply}")

        return jsonify({"reply": bot_reply})

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return jsonify({"reply": "An error occurred with the AI service. Please try again later."}), 500

    except Exception as e:
        logging.error(f"General error: {e}")
        return jsonify({"reply": "An internal error occurred. Please try again later."}), 500
