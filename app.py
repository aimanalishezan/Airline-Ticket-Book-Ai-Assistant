# Import required libraries
import os 
from dotenv import load_dotenv 
import ollama                   
import gradio as gr             
import json                     

# Load .env variables
load_dotenv()

# Get environment variables for model name and Gradio login credentials
model = os.getenv('mod')
id = os.getenv('id')
pas = os.getenv('pas')

# Set the model name
MODEL = model

# System prompt to guide the assistant's behavior
system_message = (
    "You are a helpful assistant for an airline called flighAI. "
    "Give a short, courteous answer, no more than 1 sentence. "
    "Always be accurate. If you don't know the answer, say so."
)

# Dictionary of ticket prices (for function use)
ticket_price = {
    "dhaka": "10000tk",
    "thakurgaon": "5000tk",
    "sylet": "7000tk",
    "morocco": "40000tk"
}

# Function to get the price of a ticket based on destination
def get_ticket_price(destination_city):
    city = destination_city.lower()
    return ticket_price.get(city, "Unknown") 

# JSON schema describing the function `get_ticket_price`
price_fun = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. "
                   "Call this whenever you need to know the ticket price, for example when a customer asks 'how much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to"
            }
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

# Add the function to the list of tools for the model
tool = [{"type": "function", "function": price_fun}]

# Main chat function that interacts with the model
def chat(message, history):
    # Build the conversation history with system and user message
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    
    # First model response
    response = ollama.chat(model=MODEL, messages=messages, tools=tool)
    
    # If the model is calling a tool, handle the tool call
    if "tool_calls" in response["message"]:
        message = response["message"]
        
        # Call the appropriate tool and get the tool's response
        response_tool, city = handle_tool_call(message)
        
        # Add tool call info and its result to the message history
        messages.append(message)
        messages.append(response_tool)
        
        # Call the model again with updated history including tool results
        response = ollama.chat(model=MODEL, messages=messages)
    
    # Return the final model-generated message
    return response["message"]["content"]

# Function to handle tool call and return tool-generated message
def handle_tool_call(message):
    # Print the entire message to inspect its structure
    print("Full message received:", message)
    
    # Extract the tool call from the message
    tool_call = message["tool_calls"][0]
    
    # Print the tool_call to debug its contents
    print("Tool call data:", tool_call)
    
    # Check if the 'id' key exists in the tool_call object
    if "id" in tool_call:
        tool_call_id = tool_call["id"]
    else:
        # Handle the case where 'id' does not exist
        tool_call_id = "unknown"
    
    # Extract the arguments from the tool call
    arguments = tool_call["function"]["arguments"]
    
    # Extract the destination city from arguments
    city = arguments.get("destination_city")
    
    # Get the ticket price for the city
    price = get_ticket_price(city)
    
    # Format the tool's response with the tool_call_id
    response = {
        "role": "tool",
        "tool_call_id": tool_call_id,  # Use the retrieved or default 'id'
        "content": json.dumps({
            "destination_city": city,
            "price": price
        })
    }
    
    return response, city

# Create and launch the Gradio chat interface with login protection
gr.ChatInterface(fn=chat, type="messages").launch(share=True, auth=(id, pas))
