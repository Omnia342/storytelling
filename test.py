from together import Together

client = Together(api_key='9076e16842f3345f0295d4672d1a657bbcaf76d462a53b042c67e3c68925e475')

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
      {
        "role": "user",
        "content": "What are some fun things to do in New York?"
      }
    ]
)
print(response.choices[0].message.content)