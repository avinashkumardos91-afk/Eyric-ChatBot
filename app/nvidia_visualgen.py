import requests
import io
from PIL import Image
import urllib.parse

def main():
    print("NVIDIA's hosted Stable Video Diffusion API has been deprecated.")
    print("Falling back to Pollinations.ai for High-Quality Visual Generation...")
    
    prompt = "A cat sitting on a windowsill, cinematic lighting, highly detailed, 4k"
    print(f"\nGenerating visual for prompt: '{prompt}'")
    
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)
    API_URL = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        
        # The API returns the raw image bytes
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        
        output_file = "output_visual.png"
        image.save(output_file)
        print(f"\nSuccess! Visual generated and saved to {output_file}")
        
    except requests.exceptions.HTTPError as e:
        print(f"\nError: API request failed.")
        print(f"Status Code: {e.response.status_code}")
        print(f"Details: {e.response.text}")
    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    main()
