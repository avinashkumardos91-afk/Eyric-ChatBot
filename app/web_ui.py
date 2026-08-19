import os
import requests
import urllib.parse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Constants
NVIDIA_API_KEY = "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"
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Proxy chat requests to NVIDIA API (simulating the local chat for speed in UI)"""
    data = request.json
    prompt = data.get('prompt', '')
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/visual', methods=['GET'])
def visual():
    """Generate image via Pollinations API"""
    prompt = request.args.get('prompt', '')
    
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    # Redirect straight to the image URL so the <img> tag loads it directly
    from flask import redirect
    return redirect(image_url)

@app.route('/api/explain', methods=['POST'])
def explain():
    """Use NVIDIA Llama to explain code snippets"""
    data = request.json
    code_snippet = data.get('code', '')
    
    prompt = f"Please explain the following code and add comments:\n```python\n{code_snippet}\n```"
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2048
    }
    
    try:
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure static and templates directories exist
    os.makedirs('app/templates', exist_ok=True)
    os.makedirs('app/static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
