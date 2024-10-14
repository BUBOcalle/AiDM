import gradio as gr
import random
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
import PIL
from rollplayClasses import *

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])
hero = Hero(type="hero", name="Calle Dachalin", hp=10, battleSkill=6, location="the tavern", description="a tall blonde man with a destiny", equipment=["his favourite book", "flint and steel", "some beer"], weapons=[Weapon(3, "Mighty stick")])
enemiesInScenes = {"the tavern":[]}
NPCInScenes = {"the tavern":[]}
enemies = []
NPCs = []

JSONs_from_pictures = []

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="""You are the dungeon master in a DnD campaign. Make sure to keep track of where the player and are charakters are at all time!"""
)

def createPromt(inputs, history, currentLocation):
    return f"""
        <instructions>
            Be a good dugeon master and create an epic story. Tell what happens next in the story
        <\instructions>

        <Hero character>
            {hero}
        <\Hero character>

        <Enemies in scene>
            {enemiesInScenes[currentLocation]}
        <\Enemies in scene>

        <NPC:s in scene>
            {enemiesInScenes[currentLocation]}
        <\\NPC:s in scene>

        <history of conversation>
            {history}
        <\history of conversation>

        <latest input>
            {inputs['text']}
        <\latest input>
        """

def interactionLoop(inputs, history):
    lastResponse = response(inputs, history)
    print(lastResponse)
    newCharacterEncountered(NPCs, enemies, lastResponse)
    return lastResponse

def response(inputs, history):
    return model.generate_content(createPromt(inputs, history, hero.location),
                                    generation_config=genai.types.GenerationConfig(
                                    max_output_tokens=1000,
                                    temperature=0.0,
                                    top_p=0.95
                                    ),
                                    safety_settings={
                                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                        }).text


def newCharacterEncountered(NPC, enemies, lastResponse):
    print("New character?")
    print(model.generate_content([f"ANSWER ONLY YES OR NO, are there any new characters introduced in this prompt, that are NOT in the following lists: {NPC} or {enemies}. Promt: {lastResponse}"],
                                    generation_config=genai.types.GenerationConfig(
                                    max_output_tokens=10,
                                    temperature=0.0,
                                    top_p=0.95
                                    )).text)
    



with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=interactionLoop,
        title="The epic dungeon master",
        multimodal=True
    )

if __name__ == "__main__":
    demo.launch()
