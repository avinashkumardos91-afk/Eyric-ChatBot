import sys
import os
import requests

# Set your NVIDIA API key here
API_KEY = "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"
# We'll use Llama 3.1 8B for fast, responsive code explanation
MODEL = "meta/llama-3.1-8b-instruct"
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def explain_code(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        code_content = f.read()

    print(f"Sending code to NVIDIA API ({MODEL}) for explanation...")
    
    prompt = f"""
    Please act as a Senior Software Engineer. Review the following code, and provide:
    1. A brief summary of what the code does.
    2. The code rewritten with helpful comments and Python docstrings added.

    Code to review:
    ```python
    {code_content}
    ```
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2, # Low temperature for factual, consistent code output
        "max_tokens": 2048
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        explanation = data['choices'][0]['message']['content']
        
        print("\n" + "="*50)
        print("💡 AI CODE EXPLANATION & COMMENTS")
        print("="*50 + "\n")
        print(explanation)
        print("\n" + "="*50)
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Details: {e.response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python code_explainer.py <path_to_code_file>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    explain_code(target_file)
