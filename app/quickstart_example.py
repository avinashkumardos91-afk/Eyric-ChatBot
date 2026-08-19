import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

def main():
    print("Downloading TinyLlama GGUF model for CPU inference...")
    # We use a quantized GGUF model which is optimized for CPU inference
    model_path = hf_hub_download(
        repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        filename="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    )

    print(f"Model downloaded to: {model_path}")
    print("Loading model...")
    
    # Initialize the LLM
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,  # Context window
        n_threads=os.cpu_count(), # Use all available CPU cores
        verbose=False
    )

    # Sample prompts
    prompts = [
        "Hello, my name is",
        "The capital of France is",
        "The future of AI is",
    ]

    print("\nStarting inference...")
    for prompt in prompts:
        output = llm(
            prompt,
            max_tokens=64,
            temperature=0.8,
            top_p=0.95,
            echo=False
        )
        generated_text = output['choices'][0]['text']
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

if __name__ == '__main__':
    main()
