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
modes = modeSwitcher()

inCombat = 0

def interactionLoop(inputs, history):
    if inCombat == 0:
        response = DM.generateResponse(inputs, state)
        state.updateGameState()

        # state.generateLongTermHistory(state.recent_history)
        print("Combat?")
        inCombat = modes.newMode(response)
        return response
    elif inCombat == 1:
        pass


with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        title="The epic dungeon master",
        multimodal=True
    )

if __name__ == "__main__":
    demo.launch()
