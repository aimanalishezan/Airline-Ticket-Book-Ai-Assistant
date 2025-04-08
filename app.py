import os 
from dotenv import load_dotenv
import ollama
import gradio as gr
import json
load_dotenv()

model=os.getenv('mod')
id=os.getenv('id')
pas=os.getenv('pas')

MODEL=model


system_message="you are a helpful assistant for an airline called flighAI"
system_message+="give a short, courteous answer, no more then 1 sentence."
system_message+="Always be accurate . if you don't know the answer , say so ."

#function for the tool
ticket_price={"dhaka":"10000tK","thakurgaon":"5000tk","sylet":"7000tk","morocco":"40000"}
def get_ticket_price(destination_city):
    city=destination_city.lower()
    return ticket_price.get(city,"Unknown")
#there is a particular dictionary structure thats required to describe our function 
price_fun={
    "name":"get_ticket_price",
    "description":"Get the price of a return ticket to the festination city . call this whenver your need to know the ticket price, for ecample when a customer asks ' how much is a ticket to this city'",
    "parameters":{
        "type":"object",
        "properties":{
            "destination_city":{
                "type":"string",
                "destination":"the city that the customer wants to travel to ",
            },
        },
    },
        "required":["destination_city"],
        "additionalProperties":False
}
#add function to the tools list
tool=[{"type":"function","function":price_fun}]

#gradio ui 
def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = ollama.chat(model=MODEL, messages=messages, tools=tool)
    
    if "tool_call" in response["message"]:
        message = response["message"]
        response_tool, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response_tool)
        response = ollama.chat(model=MODEL, messages=messages)
    
    return response["message"]["content"]

#function that handle tools calls

def handle_tool_call(message):
    tool_call = message["tool_call"][0]
    arguments = json.loads(tool_call["function"]["arguments"])
    city = arguments.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call["id"]
    }
    return response, city


#intigrate gradio ui 
gr.ChatInterface(fn=chat,type="messages").launch(share=True,auth=(id,pas))