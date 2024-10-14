import gradio as gr
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PIL
from rollplayClasses import *
from Ais import *

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

DM = storyTeller()
state = stateOfTheGame()
infoFetcher = infoFetcherAi()
modes = modeSwitcher()

def interactionLoop(inputs, history):
    response = DM.generateResponse(inputs, state)
    # lastResponse = DM.response(inputs, history)
    # print(lastResponse)
    # infoFetcher.newCharacterEncountered(DM.NPCs, DM.enemies, lastResponse)
    # print(infoFetcher.newCharacterEncountered(state, response))
    state.generateLongTermHistory(state.recent_history)
    print("Combat?")
    print(modes.newMode(response))
    return response


with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        title="The epic dungeon master",
        multimodal=True
    )

if __name__ == "__main__":
    demo.launch()
