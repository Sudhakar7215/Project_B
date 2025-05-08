
from flask import Flask, render_template
from chat_handler import chat_handler
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    return chat_handler()

# Run the Flask app on port 8080
if __name__ == "__main__":
    # Get the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
