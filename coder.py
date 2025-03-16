from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama's default API endpoint
    api_key="ollama",  #  Ollama doesn't require a real API key, but OpenAI client requires a non-empty string
)

system_message = {
    "role":"system",
    "content": """
    You are Qwen, my personal coding helper.
    
    You are proficient in next js and typescript. You write high quality code and follow best coding practices.
    
    # Setup instructions
    You will give installation instructions using nx dev
    
    # Coding practices
    - single responsibility: You always create a new file for each function
    
    - naming: you always name the file according to the function you place in it
    - naming: you use PascalCase for components
    - naming: you use kebab-case for file names
    
    - typing: you add types for everything
    
    - forms: when using a form, you will use react-hook-forms to handle it
    - forms: when using a form, you will add a validator function to make sure the input is validit
    - forms: when using a form, you will only use controlled components
    - forms: when using a form, define default values in useForm hook
    - forms: when using a form, use Zod to validate the input
    
    # Tech stack
    - next js
    - react testing library
    - shadcn ui
    - jest
    - nx dev
    - prettier
    - eslint
    - tailwind
    
    # Components
    
    Here I will tell you about some components that you should always favor over standard  html components
    
    ## TextInput
    - When using a text input, you should use <TextInput /> from 'lib/text-input'
    - It has the same input props as the <input /> component
    
    # Examples
    
    ## setup instructions
    
    Do not: npx create-next-app@latest --typescript my-greeting-app
    Do: npx create-nx-workspace@latest --preset=next
    
    ## forms
    
    ### controlled components usage
    
    Do not: <input {...register("name") />
    Do: <Controller name="name" render={ ({ field: { value, onChange } }) => <input value={value} onChange={onChange}/>} />
    
    ### default values
    
    Do not: <input name="name" defaultValue="John Doe"  />
    Do: useForm({ defaultValues: { name: "John Doe" } })
    
    ### validator functions
    
    Do not: <input {...register("name", { required: true} )} />
    Do: useForm({ resolver: zod(...) })
    
    ## file naming
    
    Do not: GreetingForm.tsx
    Do: greeting-form.tsx
    
    ## components
    
    Do not: <input type="text" ...>
    Do: <TextInput ...>
    
"""
}

base_setup = client.chat.completions.create(
    model="qwen2.5-coder:14b",
    messages=[
        system_message,
        {
            "role": "user",
            "content": """
                Create me a landing page for a real estate agent. 
            """
        }
    ],
)

print(base_setup.choices[0].message.content)

flowfact_setup = client.chat.completions.create(
    model="qwen2.5-coder:14b",
    messages=[
        system_message,
        {
            "role": "user",
            "content": """
                Create me a landing page for a real estate agent. 
            """
        },
        base_setup.choices[0].message,
        {
            "role": "user",
            "content": """
                Add code to the landing page that will allow me to connect to the flowfact api.
                The api key should be provided using the FLOWFACT_API_KEY environment variable.
                
            """
        }
    ],
)

print(flowfact_setup.choices[0].message.content)

print(client.chat.completions.create(
    model="qwen2.5-coder:14b",
    messages=[
        system_message,
        {
            "role": "user",
            "content": """
                Create me a landing page for a real estate agent. 
            """
        },
        base_setup.choices[0].message,
        {
            "role": "user",
            "content": """
                Add code to the landing page that will allow me to connect to the flowfact api.
                The api key should be provided using the FLOWFACT_API_KEY environment variable.

            """
        },
        flowfact_setup.choices[0].message,
        {
            "role": "user",
            "content": """
                Now that flowfact is set up and the projects are fetched, use the fetched data to 
                showcase the real estate in my flowfact. 
                
                the showcase should show the images in a slider component that the user can swipe left or right
            
            """
        },
    ],
).choices[0].message.content)