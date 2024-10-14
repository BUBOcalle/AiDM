from rollplayClasses import *
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv

# from EnemyExamples import EXAMPLES as ENEMY_EXAMPLES

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])


class stateOfTheGame():
    def __init__(self):
        self.hero = Hero(type="hero", name="Calle Dachalin", hp=10, battleSkill=6, location="the tavern", description="a tall blonde man with a destiny", equipment=["his favourite book", "flint and steel", "some beer"], weapons=[Weapon(3, "Mighty stick")])
        # self.enemiesInScenes = {"the tavern":[]}
        # self.NPCInScenes = {"the tavern":[]}
        # self.enemies = []
        # self.NPCs = []
        self.recent_history = []
        self.history = []
        self.model = genai.GenerativeModel("gemini-1.5-flash",
                                           system_instruction="You are a helper who aids a DM of a DnD game by providing various information and summarizations.")
        # self.stringRepresentationOfData = f"""Hero: {self.hero},
        #                                     Location: {self.hero.location},
        #                                     Enemies in scene: {self.enemiesInScenes},
        #                                     NPCs in scene: {self.NPCInScenes},
        #                                     """
        

    def __str__(self) -> str:
        # description = self.model.generate_content(["Given the following data explain the state of the game", self.stringRepresentationOfData],
        #                                 generation_config=genai.types.GenerationConfig(
        #                                 max_output_tokens=1000,
        #                                 temperature=0.0,
        #                                 top_p=0.95
        #                                 ),
        #                                 safety_settings={
        #                                         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        #                                         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        #                                         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        #                                         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        #                                     }).text

        description = f'Heroes: {self.hero} \nLocation: {self.hero.location}'

        return description
    

    def generateLongTermHistory(self, history):
        instructions = "Generate a summary of the events which have unfolded so far. This summary should include any events relevant to the story, "+\
            "any relevant interactions with characters, any interesting locations, any new equipment discoveries, etc. Below you will find the extended "+\
            "history which you are to summarize. Please make sure the summary is accurate and based on only what is stated in the history. "
        history_str = '\n'.join(f'{input}\n{dm}' for input, dm in history)

        prompt = f"<instructions>\n{instructions}\n</instructions>\n\n"+\
            f"<history>\n{history_str}\n</history>"
        
        history_summary = self.model.generate_content(prompt,
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

        return history_summary
    

    def updateGameState(self):
        # Did the hero recieve or lose any equipment?
        instructions = "Please analyze the story and determine if the hero lost or acquired any equipment. Consider the entire story history, "+\
            "the most recent event and the current state of the game found below. Provide two lists, first one with any new equipment and then one "+\
            "with any lost equipment on the form: \n[new_equipment_1, new_equipment_2, ...]\n[lost_equipment_1, lost_equipment_2, ...]"+\
            "\nIf no equipment is lost or gained, reply with two empty lists. Any lost equipment must match the exact name in the current hero state. "+\
            "Note that weapons do not count as equipment. "
        history_str = '\n'.join(f'{input}\n{dm}' for input, dm in self.history)
        recent_history_str = '\n'.join(f'{input}\n{dm}' for input, dm in self.recent_history)
        state = str(self)
        # examples = "The bridge swayed in the wind and the hero dropped his treasured "

        prompt = f"<instructions>\n{instructions}\n<\instructions>\n\n"+\
            f"<history>\n{history_str}\n{recent_history_str}\n</history>\n\n"+\
            f"<current state>\n{state}\n</current state>\n\n"
            # f"<examples>{examples}\n</examples>"
        equipment = self.model.generate_content(prompt,
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
        print(equipment)

        # Did the hero acquire or lose any weapons?

        # Did the location of the hero change?



class storyTeller:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash",
                                           system_instruction="You are the dungeon master in an epic DnD campaign!")

    def __str__(self):
        pass

    def createPromt(self, inputs, state):
        # Don't let the adventurer spawn new characters
        instructions = "You are the dungeon master telling the epic story of a DND adventure. Please tell the adventurers about the next scene. "+\
            "Consider the current state of the adventure and the history of what has happened so far. Don't let the heroes perform unrealistic "+\
            "actions given thier character descriptions. For instance, a knight typically cannot perform magic spells. "+\
            "The adventurers must follow your pace of the story. They are not allowed to fast-forward through events by dictating the story. "+\
            "You, the DM, control the story and will let the adventurers know if they attempt to take control of the unfolding events. "+\
            "If they have to walk through a forest to get to a location, they must go through the forest at your pace and deal "+\
            "with any encounters along the way to get there. They may not simply write 'I walked through the forest and arrived at the location'. At the bottom, you find the latest input of the adventurers."
        history_str = '\n'.join(f'{input}\n{dm}' for input, dm in state.history)
        recent_history_str = '\n'.join(f'{input}\n{dm}' for input, dm in state.recent_history)

        prompt = f"<instructions>\n{instructions}\n<\instructions>\n\n"+\
            f"<current state>\n{str(state)}\n</current state>\n\n"+\
            f"<history>\n{history_str}\n{recent_history_str}\n</history>\n\n"+\
            f"<input>\n{inputs['text']}\n</input>"
        
        print(prompt)

        return prompt


    def generateResponse(self, inputs, state):
        prompt = self.createPromt(inputs, state)
        response = self.model.generate_content(prompt,
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
        
        state.recent_history.append((f"Input: {inputs['text']}", f'DM: {response}'))

        return response
    

class infoFetcherAi:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def __str__(self):
        pass

    def EnemiesForCombat(self, currentState, lastResponse, enemyList):
        instructions = "You are a helper to a dungeon master in DnD, and your task is to give reasonable stats to enemies before combat." +\
            "The enemies should be printed in EXACTLY this format:"+\
            "name/title:value, hp:value, battleSkill:value, damageOutput:value" +\
            "To help you, you can read the story so far. It will be in the text section." +\
            "The name/title is the only one you can probabably find in the story. The other values you have to come up with yourself." +\
            "Use the name/title of the character, and the examples below to generate the values. Try to be realistic. A bear should be much stronger than a human. A goblin should be slightly weaker than a human, etc."    
        examples = '\n'.join(line[0] for line in ENEMY_EXAMPLES)

        prompt = f"<instructions>\n{instructions}\n</instructions>\n\n"+\
            f"<enemiesToGiveStats>\n{enemyList}\n</enemiesToGiveStats>\n\n"+\
            f"<text>\n{lastResponse}\n</text>\n\n"+\
            f"<examples>\n{examples}\n</examples>"
        print(prompt)
        new_characters = self.model.generate_content(prompt,
                                                    generation_config=genai.types.GenerationConfig(
                                                        max_output_tokens=100,
                                                        temperature=0.0,
                                                        top_p=0.95
                                                    )).text
        return new_characters


class modeSwitcher():
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def __str__(self):
        pass

    def newMode(self, response):
        fightTest = self.model.generate_content(f"Did this encounter start a combat or a fight? Encounter: {response}. IF NO PRINT 'NO.', IF YES PRINT A LIST OF THE ENEMIES IN THE ENCOUNTEREr IN THE FORM ['enemie1', 'enemie2']",
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
        
        if fightTest[0] == "[":
            print
        #start combat
        pass


if __name__=='__main__':
    DM = storyTeller()
    state = stateOfTheGame()

    inputs = {'text': 'Begin the adventure!'}
    currentState = str(state)
    print(DM.createPromt(inputs, currentState))
    genai.configure(api_key=os.environ["API_KEY"])
    print(DM.generateResponse(inputs, currentState))