import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

# --- Configuration & Initialization ---
# IMPORTANT: For production, use environment variables to store your API Key.
API_KEY = "Enter your API KEY HERE" 
genai.configure(api_key=API_KEY)

app = Flask(__name__)

# Initialize the Gemini model and a persistent chat session
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
    chat_session = model.start_chat()
    print("Gemini chat session initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    chat_session = None

# --- Route to serve the Frontend (The Link) ---
@app.route('/')
def serve_frontend():
    """Serves the index.html file from the same directory."""
    # This route allows the user to simply navigate to http://127.0.0.1:5000/
    return send_from_directory('.', 'index.html') 

# --- API Endpoint to Handle Chat Messages ---
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """Processes the user message and gets a response from the AI."""
    if not chat_session:
        return jsonify({"error": "Chat service is not initialized."}), 500

    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    try:
        # Send the message to the Gemini chat session
        response = chat_session.send_message(user_input)
        
        # Return the AI's response text to the frontend
        return jsonify({
            "response": response.text
        })
    except Exception as e:
        print(f"Error during chat interaction: {e}")
        return jsonify({"error": "An error occurred during the AI interaction."}), 500

if __name__ == '__main__':
    # Runs the server on http://127.0.0.1:5000/
    app.run(debug=True)

