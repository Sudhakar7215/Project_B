
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
    port = int(os.environ.get("PORT", 8080))
    print(f"App running at http://127.0.0.1:{port}")
    app.run(debug=True, host="0.0.0.0", port=8080,use_reloader=False)

