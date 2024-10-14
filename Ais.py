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
        self.model = genai.GenerativeModel(
                    "gemini-1.5-flash",
                    system_instruction="""You are the dungeon master in a DnD campaign. Make sure to keep track of where the player and are charakters are at all time!""")
        pass
    
    def __str__(self):
        pass

    def createPromt(self, inputs, history, currentLocation):
        return f"""
            <instructions>
                Be a good dugeon master and create an epic story. Tell what happens next in the story
            <\instructions>

            <Hero character>
                {self.hero}
            <\Hero character>

            <Enemies in scene>
                {self.enemiesInScenes[currentLocation]}
            <\Enemies in scene>

            <NPC:s in scene>
                {self.enemiesInScenes[currentLocation]}
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