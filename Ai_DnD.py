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
        modes.inCombat = modes.newMode(response, state) # For now passed state as function to keep track of enemies

        return response
    elif modes.inCombat == 1:
        combatScene = CombatScene(state.hero, state.hero.weapons[0], state.enemies, "hero")
        combatScene.combat()


with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        title="The epic dungeon master",
        multimodal=True
    )

if __name__ == "__main__":
    demo.launch()
