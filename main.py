from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama's default API endpoint
    api_key="ollama",  #  Ollama doesn't require a real API key, but OpenAI client requires a non-empty string
)

system_message = {
    "role": "system",
    "content":
        """
            You are a specialist in marketing an brand building.
        
            Output only what the user asks for in the output specification without any flavor text    
       """
}



# demo chat completion with streaming
response = client.chat.completions.create(
    model="qwen2.5",
    messages=[
        system_message,
        {
            "role": "user",
            "content": """
                Suggest me a list of 10 names for shoe companies.
                
                Example: 
                IShoes
            """
        }
    ],
)

shoe_companies = response.choices[0].message.content

response_2 = client.chat.completions.create(
    model="qwen2.5",
    messages=[
        system_message,
        {
            "role": "assistent",
            "content": shoe_companies
        },
        {
            "role": "user",
            "content": f"""
                Take this list of names for shoe company names.
                
                Rate them on an out of 10 scale.
                List me three titles for marketing campaigns for each title.
                Order the names by their rating, starting with the best
                
                Example: 
                
                1. iShoes - 9/10 - Quality shoes as special as you, special shoes, the new deal
            """
        }
    ],
)

with_rating = response_2.choices[0].message.content

response_3 = client.chat.completions.create(
    model="qwen2.5",
    messages=[
        system_message,
        {
            "role": "assistent",
            "content": shoe_companies
        },
        {
            "role": "user",
            "content": f"""
                Take this list of names for shoe company names.

                Rate them on an out of 10 scale.
                List me three titles for marketing campaigns for each title.
                Order the names by their rating, starting with the best

                Example: 

                1. iShoes - 9/10 - Quality shoes as special as you, special shoes, the new deal
            """
        },
        {
            "role": "assistent",
            "content": with_rating
        },
        {
            "role": "user",
            "content": f"""
                Take the top  result of the shoe company rating list.
                
                Create me a good marketing campaign for a young target audience
            """
        },
    ],
)

print(response_3.choices[0].message.content)