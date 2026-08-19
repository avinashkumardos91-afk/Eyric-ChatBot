import os
from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.environ.get("NVIDIA_API_KEY")
)

try:
    completion = client.chat.completions.create(
      model="nvidia/nemotron-3-ultra-550b-a55b",
      messages=[{"role":"user","content":"Write a limerick about the wonders of GPU computing."}],
      temperature=1,
      top_p=0.95,
      max_tokens=1024,
    )
    print("\n--- Output ---")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
