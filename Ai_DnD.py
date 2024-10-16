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


# introduction = DM.generateResponse({"text": "Begin the adventure!"}, state)
# state.history = state.recent_history
# state.recent_history = []

# introduction = 'Test'

def interactionLoop(inputs, history):
    if state.hero.hp <= 0:
        return DM.model.generate_content("Explain for the player how incredibly Dead he is. Explain it in a funny way with some jokes. Don't talk about how he died just that he is dead!",
                                                generation_config=genai.types.GenerationConfig(
                                                max_output_tokens=1000,
                                                temperature=0.5,
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
        modes.inCombat = modes.newMode(response, state) # For now passed state as function to keep track of enemies
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

            #    "#component-0, #component-3, #component-10, #component-8  { height: 100% !important; }"

# with gr.Blocks(title='The Epic Dungeon Master',
#                css=".contain { display: flex !important; flex-direction: column !important; }"
#                "#component-1 { height: 100% !important; }"
#                "#chatbot { flex-grow: 1 !important; overflow: auto !important;}"
#                "#col { height: 100vh !important; }") as demo:
#     gr.Markdown("# The Epic Dungeon Master")
with gr.Blocks(fill_height=True) as demo:
    # with gr.Row(equal_height=False):
    #     with gr.Column(scale=1, elem_id='col'):
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        multimodal=True,
        title='The Epic Dungeon Master',
        # chatbot=gr.Chatbot(value=[(None, introduction)],
        #                 label='The Epic Dungeon Master')
    )


if __name__ == "__main__":
    demo.launch()
