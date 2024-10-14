import gradio as gr
import random
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
import PIL
from rollplayClasses import *
from Ais import *

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

DM = storyTeller()
infoFetcher = infoFetcherAi()

def interactionLoop(inputs, history):
    lastResponse = DM.response(inputs, history)
    print(lastResponse)
    infoFetcher.newCharacterEncountered(DM.NPCs, DM.enemies, lastResponse)
    return lastResponse


with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        title="The epic dungeon master",
        multimodal=True
    )

if __name__ == "__main__":
    demo.launch()
