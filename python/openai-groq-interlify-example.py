import json
from openai
from interlify import Interlify

ACCESS_TOKEN="YOUR_API_ACCESS_TOKEN"

model = "llama-3.3-70b-versatile"


client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="YOUR_GROQ_API_KEY",
)

# Initialize the client
interlify = Interlify(
    api_key="INTERLIFY_API_KEY",
    project_id="PROJECT_ID",
    auth_headers=[
        {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    ]
    
)

# Prepare the tools
tools = interlify.get_tools()


messages = [
    {"role": "system", "content": "You are a shoe shop assistant."},
    {"role": "user", "content": "update the second shoe price to 100"},
]


response = client.chat.completions.create(
    model=model, messages=messages, tools=tools, tool_choice="auto"
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls
messages.append(response_message)

for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # Call the tool
    function_response = interlify.call_tool(function_name, function_args)

    messages.append(
        {
            "role": "tool",
            "content": str(function_response),
            "tool_call_id": tool_call.id,
        }
    )

# Make the final request with tool call results
final_response = client.chat.completions.create(
    model=model, messages=messages, tools=tools, tool_choice="auto"
)

print(final_response.choices[0].message.content)

