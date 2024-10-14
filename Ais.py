from rollplayClasses import *
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv

from newCharacterEncountered_Examples import EXAMPLES as NEW_CHARACTER_EXAMPLES

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



class storyTeller:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash",
                                           system_instruction="You are the dungeon master in an epic DnD campaign!")

    def __str__(self):
        pass

    def createPromt(self, inputs, state):
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

    # def newCharacterEncountered(self, currentState, lastResponse):
    #     # print("New character?")
    #     # print(self.model.generate_content([f"ANSWER ONLY YES OR NO, are there any new characters introduced in this prompt, that are NOT in the following lists: {NPC} or {enemies}. Promt: {lastResponse}"],
    #     #                                 generation_config=genai.types.GenerationConfig(
    #     #                                 max_output_tokens=10,
    #     #                                 temperature=0.0,
    #     #                                 top_p=0.95
    #     #                                 )).text)
        
    #     instructions = "You are a story analyst tasked with finding out if a new piece of the story introduces any new characters. "+\
    #         "Please provide a list of any NEW characters relevant to the story. Consider the list of known "+\
    #         "characters below. The text to analyze is found at the bottom. "+\
    #         "Produce a list on the form: [character1, character2, ...], or simply [] if no new characters were introduced. "
    #     examples = '\n'.join(f'{text}\n{characters}' for text, characters in NEW_CHARACTER_EXAMPLES)

    #     prompt = f"<instructions>\n{instructions}\n</instructions>\n\n"+\
    #         f"<characters>\n{currentState.NPCs}\n{currentState.hero}\n</characters>\n\n"+\
    #         f"<text>\n{lastResponse}\n</text>\n\n"+\
    #         f"<examples>\n{examples}\n</examples>"
    #     print(prompt)
    #     new_characters = self.model.generate_content(prompt,
    #                                                  generation_config=genai.types.GenerationConfig(
    #                                                     max_output_tokens=100,
    #                                                     temperature=0.0,
    #                                                     top_p=0.95
    #                                                  )).text
    #     return new_characters


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