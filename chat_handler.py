import openai
from dotenv import load_dotenv
import os
from flask import request, jsonify
import logging
from token_usage import extract_token_usage, estimate_cost


# Set your OpenAI API key (Make sure to replace this with your actual key or set it using environment variables)
load_dotenv(dotenv_path="confidential.env")  # Load environment variables from .env

openai.api_key = os.getenv('openai_api_key')
# Configure logging to show debug messages
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='chitti_logs.log',
                    filemode='a'  # use 'w' to overwrite each run if needed
                    )

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
        # Get token usage and cost
        token_info = extract_token_usage(response)
        cost = estimate_cost(
            token_info['prompt_tokens'],
            token_info['completion_tokens']
        )
        logging.debug(f"Bot response: {bot_reply}")
        logging.debug(f"Token usage: {token_info}")
        logging.debug(f"Estimated cost: ${cost}")
        return jsonify({"reply": bot_reply,**token_info,"estimated_cost_usd":cost})

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return jsonify({"reply": "An error occurred with the AI service. Please try again later."}), 500

    except Exception as e:
        logging.error(f"General error: {e}")
        return jsonify({"reply": "An internal error occurred. Please try again later."}), 500
    
def get_bot_response(user_input, chat_history):
    messages = [{"role": "system", "content": "You are Chitti, an expert in cars."}]
    for role, content in chat_history:
        messages.append({"role": role, "content": content})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']
