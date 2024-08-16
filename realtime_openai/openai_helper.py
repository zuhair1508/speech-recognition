from openai import OpenAI
from api_secrets import API_KEY_OPENAI

client = OpenAI(api_key=API_KEY_OPENAI)

def ask_computer(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Please provide a response based only on verified facts and evidence. Avoid speculation or opinion, and include references or citations if possible to support the information shared."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=100,
    )
    return response.choices[0].message.content
    
    