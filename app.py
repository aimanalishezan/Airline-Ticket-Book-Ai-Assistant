import os 
from dotenv import load_dotenv
import ollama
import gradio as gr

load_dotenv()

model=os.getenv('mod')


MODEL=model


system_message="you are a helpful assistant for an airline called flighAI"
system_message+="give a short, courteous answer, no more then 1 sentence."
system_message+="Always be accurate . if you don't know the answer , say so ."

#function for the tool
ticket_price={"dhaka":"10000tK","thakurgaon":"5000tk","sylet":"7000tk","morocco":"40000"}