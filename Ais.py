from rollplayClasses import *
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

class storyTeller:
    def __init__(self):
        self.hero = Hero(type="hero", name="Calle Dachalin", hp=10, battleSkill=6, location="the tavern", description="a tall blonde man with a destiny", equipment=["his favourite book", "flint and steel", "some beer"], weapons=[Weapon(3, "Mighty stick")])
        self.enemiesInScenes = {"the tavern":[]}
        self.NPCInScenes = {"the tavern":[]}
        self.enemies = []
        self.NPCs = []
        self.model = genai.GenerativeModel("gemini-1.5-flash",
                                           system_instruction="""You are the dungeon master in an epic DnD campaign!""")
        self.history = []
    
    def __str__(self):
        pass

    def createPromt(self, inputs, currentState, history):
        prompt = f"""
                <instructions>
                    You are the dungeon master telling the epic story of a DND adventure. Please tell the adventurers about the next scene. 
                    Consider the current state of the adventure and the history of what has happened so far. At the bottom, you find the 
                    latest action of the adventurers. 
                <\instructions>

                <current state>
                    {currentState}
                </current state>

                <history>
                    {history}
                </history>

                <action>
                    {inputs['text']}
                </action>
                """

                # <Hero character>
                #     {self.hero}
                # <\Hero character>

                # <Enemies in scene>
                #     {self.enemiesInScenes[currentLocation]}
                # <\Enemies in scene>

                # <NPC:s in scene>
                #     {self.enemiesInScenes[currentLocation]}
                # <\\NPC:s in scene>

                # <history of conversation>
                #     {history}
                # <\history of conversation>

                # <latest input>
                #     {inputs['text']}
                # <\latest input>
        
        return prompt


    def generateResponse(self, inputs, currentState, history):
        response = self.model.generate_content(self.createPromt(inputs, currentState, history),
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
        
        return response

class infoFetcherAi:
    def __init__(self):
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="""""")
        pass
    
    def __str__(self):
        pass

    def newCharacterEncountered(self, NPC, enemies, lastResponse):
        print("New character?")
        print(self.model.generate_content([f"ANSWER ONLY YES OR NO, are there any new characters introduced in this prompt, that are NOT in the following lists: {NPC} or {enemies}. Promt: {lastResponse}"],
                                        generation_config=genai.types.GenerationConfig(
                                        max_output_tokens=10,
                                        temperature=0.0,
                                        top_p=0.95
                                        )).text)

import os

if __name__=='__main__':
    DM = storyTeller()
    inputs = {'text': 'Begin the adventure!'}
    currentState = 'The adventure begins inside of a tavern'
    history = []
    print(DM.createPromt(inputs, currentState, history))
    genai.configure(api_key=os.environ["API_KEY"])
    print(DM.response(inputs, currentState, history))