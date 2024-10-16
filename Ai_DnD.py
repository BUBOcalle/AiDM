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
CS = CombatScene()


def interactionLoop(inputs, history):
    if state.hero.hp <= 0:
        return DM.model.generate_content("Explain for the player how incredibly Dead he is. Explain it in a funny way with some jokes. Don't talk about how he died just that he is dead!",
                                                generation_config=genai.types.GenerationConfig(
                                                max_output_tokens=1000,
                                                temperature=0.3,
                                                top_p=0.95
                                                ),
                                                safety_settings={
                                                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                    HarmCategory.HARM_CATEGORY_HARASSMENT:  HarmBlockThreshold.BLOCK_NONE,
                                                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                                }).text

    combatStart = ""
    if modes.inCombat == 0:
        response = DM.generateResponse(inputs, state)
        state.updateGameState()
        modes.inCombat = modes.newMode(response, state)
        if (modes.inCombat):
            wdyd = response.find("What do you do?")
            if(wdyd != -1):
                response = response[:wdyd]
            CS.hero = state.hero
            CS.currentWeapon = state.hero.weapons[0]
            CS.enemies = state.enemies
            CS.turn = "hero"
            history_summary = state.generateLongTermHistory(state.recent_history)
            state.history.append(history_summary)
            state.recent_history = []
            combatStart = CS.combatStart()

        return response + combatStart
        
    if modes.inCombat == 1:
        print(inputs)
        output, modes.inCombat = CS.curentCombatState(inputs['text'])
        # send combatState to history
        state.history.append(output)
        print(output)
        return output

with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        multimodal=True,
        title='The Epic Dungeon Master',
    )


if __name__ == "__main__":
    demo.launch()
