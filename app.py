from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

# .env file load pannu
load_dotenv()

app = Flask(__name__)

# .env file‑la irundhu API key vaangi use pannu
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are ZARA CHATBOT, a helpful AI assistant. User says: {user_message}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            reply = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply})
        else:
            return jsonify({
                "reply": f"❌ Gemini API Error. Status: {response.status_code}, Response: {response.text}"
            })
    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
