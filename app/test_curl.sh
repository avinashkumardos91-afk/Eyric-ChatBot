invoke_url='https://integrate.api.nvidia.com/v1/chat/completions'

payload=$(cat <<'JSON'
{
  "model": "nvidia/nemotron-3-ultra-550b-a55b",
  "messages": [{"role":"user","content":"Write a limerick about the wonders of GPU computing."}],
  "temperature": 1,
  "top_p": 0.95,
  "max_tokens": 16384,
  "reasoning_budget": 16384,
  "chat_template_kwargs": {"enable_thinking":true},
  "stream": true
}
JSON
)

curl -sS -N \
  --request POST \
  --url "$invoke_url" \
  --header "Authorization: Bearer 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" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --data "$payload"
