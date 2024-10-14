from rollplayClasses import *
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])


class stateOfTheGame():
    def __init__(self):
        self.hero = Hero(type="hero", name="Calle Dachalin", hp=10, battleSkill=6, location="the tavern", description="a tall blonde man with a destiny", equipment=["his favourite book", "flint and steel", "some beer"], weapons=[Weapon(3, "Mighty stick")])
        self.enemiesInScenes = {"the tavern":[]}
        self.NPCInScenes = {"the tavern":[]}
        self.enemies = []
        self.NPCs = []
        self.model = genai.GenerativeModel(
                    "gemini-1.5-flash",
                    system_instruction="""You will give information to the DM of a game, the information is not for the player""")
        self.stringRepresentationOfData = f"""Hero: {self.hero},
                                            Location: {self.hero.location},
                                            Enemies in scene: {self.enemiesInScenes},
                                            NPCs in scene: {self.NPCInScenes},
                                            """
    def __str__(self) -> str:
        return  self.model.generate_content(["Given the following data explain the state of the game", self.stringRepresentationOfData],
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
   
        

class storyTeller:
    def __init__(self):
        self.model = genai.GenerativeModel(
                    "gemini-1.5-flash",
                    system_instruction="""You are the dungeon master in a DnD campaign. Make sure to keep track of where the player and are charakters are at all time!""")
        pass
    
    def __str__(self):
        pass

    def createPromt(self, inputs, history, stateOfTheGame):
        return f"""
            <instructions>
                Be a good dungeon master and create an epic story. Tell what happens next in the story
            <\instructions>

            <Hero character>
                {stateOfTheGame.hero}
            <\Hero character>

            <Enemies in scene>
                {stateOfTheGame.enemiesInScenes[stateOfTheGame.hero.location]}
            <\Enemies in scene>

            <NPC:s in scene>
                {stateOfTheGame.enemiesInScenes[stateOfTheGame.hero.location]}
            <\\NPC:s in scene>

            <history of conversation>
                {history}
            <\history of conversation>

            <latest input>
                {inputs['text']}
            <\latest input>
            """
    def response(self, inputs, history):
        return self.model.generate_content(self.createPromt(inputs, history, self.hero.location),
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
        
        

SotG = stateOfTheGame()
print(SotG)