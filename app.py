from flask import Flask, render_template, request, jsonify
from newspaper import Article
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum" 
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") 

def summarize_text(text):
    """Diplomatic-style summarization with proper error handling"""
    if not API_KEY:
        return {"error": "API key not configured"}, 503

    try:
        prompt = (
            "You are a senior diplomatic advisor preparing briefings for government officials. "
            "Summarize the article with: "
            "1. Core Issue, 2. Key Stakeholders, 3. Immediate Implications, "
            "4. Strategic Considerations, and actionable recommendations. "
            "Maintain strict neutrality, use formal language, include verifiable facts, "
            "and keep under 200 words.\n\n"
        )
        
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "inputs": prompt + text[:2048],
                "parameters": {
                    "truncation": True,
                    "max_length": 200,
                    "min_length": 100,
                    "temperature": 0.3,
                    "no_repeat_ngram_size": 3,
                },
            },
        )

        if response.status_code != 200:
            error_msg = response.json().get("error", "API request failed")
            return {"error": f"Summarization service error: {error_msg}"}, response.status_code

        result = response.json()
        if "summary_text" in result[0]:
            return {"summary": result[0]["summary_text"]}, 200
        else:
            return {"error": "Unexpected API response format"}, 500

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}, 503
    except Exception as e:
        return {"error": f"Processing error: {str(e)}"}, 500

@app.route("/summarize", methods=["POST"])
def handle_summarize():
    """Handle diplomatic-style article summarization"""
    url = request.form.get("url")

    if not url or not url.startswith(("http://", "https://")): 
        return jsonify({"error": "Please enter a valid URL"}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()

        if not article.text:
            return jsonify({"error": "Failed to extract article content"}), 400

        summary_result, status_code = summarize_text(article.text)

        if status_code != 200:
            return jsonify(summary_result), status_code

        return jsonify(
            {
                "title": article.title,
                "summary": summary_result["summary"],
                "url": url,
                "success": True,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Error processing article: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)