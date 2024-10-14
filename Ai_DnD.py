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


def interactionLoop(inputs, history):
    if modes.inCombat == 0:
        response = DM.generateResponse(inputs, state)
        state.updateGameState()

        # state.generateLongTermHistory(state.recent_history)
        print("Combat?")
        modes.inCombat = modes.newMode(response)
        return response
    elif modes.inCombat == 1:
        #Fightingmode
        pass


with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        title="The epic dungeon master",
        multimodal=True
    )

if __name__ == "__main__":
    demo.launch()
