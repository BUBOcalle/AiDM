import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
from rollplayClasses import *
from Ais import *

# Load api key form .env file
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

# Define instances of storyteller, state of the game, game modes and combat scene.
DM = storyTeller()
state = stateOfTheGame()
modes = modeSwitcher()
CS = CombatScene()


# Interacts with gradio interface and user
def interactionLoop(inputs, history):
    # If the hero is dead, the game is not supposed to continue. Let the user know he is a fool for trying to keep on playing. 
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

    # Story telling mode
    if modes.inCombat == 0:
        # Generate response based on user input
        response = DM.generateResponse(inputs, state)
        # Update state of the game
        state.updateGameState()
        # Check if combat is initiated
        modes.inCombat = modes.newMode(response, state)

        # If combat has been initiated, 
        if (modes.inCombat):
            # Set up battle scene
            wdyd = response.find("What do you do?")
            if(wdyd != -1):
                response = response[:wdyd]
            CS.hero = state.hero
            CS.currentWeapon = state.hero.weapons[0]
            CS.enemies = state.enemies
            CS.turn = "hero"

            # Start of battle marks a milestone, history should be summarized before battle is started
            history_summary = state.generateLongTermHistory(state.recent_history)
            state.history.append(history_summary)
            state.recent_history = []

            # Start combat
            combatStart = CS.combatStart()
            # Return DM response plus first round of battle
            return response + combatStart
        
        # If not in combat, simply return the DM response
        return response
    
    # Combat mode
    if modes.inCombat == 1:
        # Proceed with next combat round
        output, modes.inCombat = CS.curentCombatState(inputs['text'])
        # Add combat round description to recent history
        state.recent_history.append(output)
        # If battle is over, summarize battle and add it to the long term history
        if not modes.inCombat:
            combat_summary = state.generateCombatSummary(state.recent_history)
            state.history.append(combat_summary)
            state.recent_history = []

            response = DM.generateResponse({'text': 'I look around. '}, state)

            return output + response
        # Return output describing the combat round
        return output

with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        multimodal=True,
        title='The Epic Dungeon Master',
    )

if __name__ == "__main__":
    demo.launch()
