import os
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Constants
NVIDIA_API_KEY = "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"
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
# Default proxy port
PORT = 8000

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    """
    Catch-all route that intercepts incoming API requests and forwards them to NVIDIA.
    """
    print(f"[TLS Proxy] Intercepting request to: /{path}")
    
    # In a real deep integration, this is where we would translate the JSON body
    # from Antigravity/Gemini specific formats to OpenAI/NVIDIA compatible formats.
    # For now, we will simply pass through any chat completion payloads directly to NVIDIA.
    
    # Get JSON payload
    data = request.get_json(silent=True) or {}
    
    # Enforce NVIDIA compatibility
    if not data.get("model"):
        data["model"] = "meta/llama-3.1-8b-instruct"
        
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        print(f"[TLS Proxy] Forwarding to NVIDIA NIM API...")
        # Send to NVIDIA
        nvidia_res = requests.post(
            NVIDIA_API_URL, 
            json=data, 
            headers=headers, 
            timeout=30,
            stream=request.args.get('stream', 'false').lower() == 'true'
        )
        
        # If streaming, yield chunks
        if nvidia_res.iter_content:
            def generate():
                for chunk in nvidia_res.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk
            return Response(generate(), status=nvidia_res.status_code, headers=dict(nvidia_res.headers))
            
        # Return standard JSON response
        nvidia_res.raise_for_status()
        print("[TLS Proxy] Request successful!")
        return jsonify(nvidia_res.json()), nvidia_res.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"[TLS Proxy] Error: {str(e)}")
        error_msg = {"error": "Failed to proxy request to NVIDIA API", "details": str(e)}
        return jsonify(error_msg), 500

if __name__ == '__main__':
    print(f"==================================================")
    print(f" NVIDIA TLS Proxy Server Starting...")
    print(f" Listening on http://127.0.0.1:{PORT}")
    print(f" Forwarding traffic to {NVIDIA_API_URL}")
    print(f"==================================================")
    
    # In production, use ssl_context='adhoc' for TLS (HTTPS)
    app.run(host='0.0.0.0', port=PORT, debug=False)
