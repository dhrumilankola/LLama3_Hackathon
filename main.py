import os
from together import Together

client = Together(api_key=os.environ.get('6cf2b0fe76f0c35a77305b34d0e2c92b90ac8193e681f332d45940efc4a67ee0'))

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
    messages=[],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>"],
    stream=True
)
print(response.choices[0].message.content)