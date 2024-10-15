from rollplayClasses import *
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import ast, json
from dotenv import load_dotenv
from ast import literal_eval

from EnemyExamples import EXAMPLES as ENEMY_EXAMPLES

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
        # Did the hero recieve or lose any equipment or weapons?
        instructions = "Please help the DM determine if the hero lost or acquired any equipment or weapons by examining the latest event in the adventure. "+\
            "Carefully consider the information below, a description of the event and the current state of the character, including their current equipment and weapons. "+\
            "Provide four lists in JSON format:\n{\nnew_equipment: [item1, item2, ...],\nlost_equipment: [item1, item2, ...],\nnew_weapons: [weapon1, weapon2, ...],\n lost_weapons: [weapon1, weapon2, ...]\n}"+\
            "If no equipment or weapon is lost or gained, reply with empty lists in the JSON. Any lost equipment or weapons must match the exact name in the current hero state. "+\
            "Any new equipment or weapons should not already exist in the hero's equipment or weapon list. Make sure that the hero is truly in possesion of a new item before adding them, "+\
            "for instance the hero is not in possession of something he wants to buy until he has paid or stolen the item. "+\
            "Make sure that the hero is truly no longer in possession of one of their items before removing them. Note that a weapon is not considered to be an equipment and should only "+\
            "be added to one list. The hero may carry multiple weapons at once, an old weapon is not lost simply because the hero acquires a new one. "+\
            "Reply with ONLY the JSON, no other words, empty spaces, blank lines or anything else. "
        recent_history_str = f"{self.recent_history[-1][1]}"
        state = str(self)

        prompt = f"<instructions>\n{instructions}\n<\instructions>\n\n"+\
            f"<event>\n{recent_history_str}\n</event>\n\n"+\
            f"<current state>\n{state}\n</current state>\n\n"
        print(prompt)
        item_update = self.model.generate_content(prompt,
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

        try:
            item_json = json.loads(item_update)
            required_keys = ['new_equipment', 'lost_equipment', 'new_weapons', 'lost_weapons']
            if not isinstance(item_json, dict):
                raise ValueError("The input should be a JSON object.")
            for key in required_keys:
                if key not in item_json:
                    raise ValueError(f"Missing '{key}' key in the JSON object.")
                if not isinstance(item_json[key], list):
                    raise ValueError(f"'{key}' should be a list.")
                if not all(isinstance(item, str) for item in item_json[key]):
                    raise ValueError(f"All items in '{key}' must be strings.")
            new_equipment = item_json['new_equipment']
            lost_equipment = item_json['lost_equipment']
            new_weapons = item_json['new_weapons']
            lost_weapons = item_json['lost_weapons']
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")
        except ValueError as e:
            raise ValueError(f"Validation error: {e}")
        
        for item in new_equipment:
            self.hero.equipment.append(item)

        for item in lost_equipment:
            if item not in self.hero.equipment:
                raise ValueError('Lost item not in hero equipment.')
            else:
                self.hero.equipment.remove(item)

        for item in new_weapons:
            try:
                elements = item.split(',')
                if len(elements) != 2:
                    raise ValueError("Input must contain both name and damage.")
                name_part = elements[0].strip()
                if not name_part.startswith("name:"):
                    raise ValueError("Missing 'name:' prefix.")
                name = name_part.split("name:")[1].strip()
                damage_part = elements[1].strip()
                if not damage_part.startswith("damage:"):
                    raise ValueError("Missing 'damage:' prefix.")
                damage = int(damage_part.split("damage:")[1].strip())
                self.hero.weapons.append(Weapon(damage, name))
            except ValueError as e:
                raise ValueError(f"Error parsing string: {e}")
        
        for item in lost_weapons:
            try:
                elements = item.split(',')
                if len(elements) != 2:
                    raise ValueError("Input must contain both name and damage.")
                name_part = elements[0].strip()
                if not name_part.startswith("name:"):
                    raise ValueError("Missing 'name:' prefix.")
                name = name_part.split("name:")[1].strip()
                damage_part = elements[1].strip()
                if not damage_part.startswith("damage:"):
                    raise ValueError("Missing 'damage:' prefix.")
                damage = int(damage_part.split("damage:")[1].strip())
                for weapon in self.hero.weapons:
                    if weapon.name == name and weapon.damage == damage:
                        self.hero.weapons.remove(weapon)
            except ValueError as e:
                raise ValueError(f"Error parsing string: {e}")


        # Did the location of the hero change?
        instructions = "You are a very professional assistant who helps the DM with various tasks. Please help the DM determine the current location of the hero. "+\
            "Consider the latest event in the adventure and the last location of the hero below. It is important that your response describes the true and current "+\
            "location of the hero, and not the location of someone else, a potential future location, topic of a conversation or similar. Only the current location of the hero. "+\
            "Reply with the updated location only. If the location has not changed compared to the last location, reply with the last location. Consider the examples "+\
            "at the end of the instructions to format your response."
        recent_history_str = '\n'.join(f'{input}\n{dm}' for input, dm in self.recent_history)
        examples = """event: The air in the tavern is thick with the scent of ale and wood smoke. A roaring fire crackles in the hearth, casting flickering shadows across the rough-hewn wooden tables. A motley crew of adventurers, merchants, and weary travelers fill the space, their voices blending into a cacophony of chatter and laughter. Calle, you find yourself drawn to a corner table where a group of men in worn leather armor are huddled around a tankard of ale, their faces etched with worry. One of them, a burly man with a thick beard and a scar running across his cheek, catches your eye and gestures for you to join them. "You look like a man who's seen his share of trouble," he says, his voice gruff but friendly. "Care to join us for a drink?" What do you do?"""+\
            "\nlast location: the tavern"+\
            '\nassistant: "the tavern"\n\n'+\
            """The tavern door creaks open, letting in a gust of cool night air. The moon hangs high in the sky, casting an ethereal glow over the cobblestone streets. A few stragglers are still out and about, their voices echoing in the quiet night. You step out onto the street, taking a deep breath of the crisp air. The tavern's warmth fades behind you, replaced by the cool night air. You can see the Blacksmith's Inn in the distance, its lights twinkling like fireflies in the darkness. What do you do next?"""+\
            "\nlast location: the tavern"+\
            '\nassistant: "the streets of a small town"\n\n'+\
            """"It's the goblins," the burly man says, his voice dropping to a whisper. "They've been getting bolder lately, raiding the outskirts of the city. We've lost several farmers and their livestock. The city guard is stretched thin, and they're not equipped to deal with this kind of threat." He takes a deep breath and continues, "We're a group of adventurers, and we've been tasked with putting a stop to this goblin menace. We need someone with your strength and courage to join us. We're heading out to the goblin caves tomorrow morning. Will you join us?" """+\
            "\nlast location: the bustling marketplace"+\
            '\nassistant: "the bustling marketplace"\n\n'

        prompt = f"<instructions>\n{instructions}\n<\instructions>\n\n"+\
            f"<events>\n{recent_history_str}\n</events>\n\n"+\
            f"<last location>\n{self.hero.location}\n</last location>\n\n"+\
            f"<examples>\n{examples}\n</examples>\n\n"
        print(prompt)
        location_update = self.model.generate_content(prompt,
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
        
        try:
            location = location_update.strip().strip('"').strip()
            self.hero.location = location
        except ValueError as e:
            raise ValueError(f"Error parsing new location: {e}")

        print(item_update)

        print(location_update)

        print(self)



class storyTeller:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash",
                                           system_instruction="You are the dungeon master in an epic DnD campaign!")
        self.image_model = genai.ImageGenerationModel("imagen-3.0-generate-001")

    def __str__(self):
        pass

    def createPromt(self, inputs, state):
        # Don't let the adventurer spawn new characters
        instructions = "You are the dungeon master telling the epic story of a DND adventure. Please tell the adventurer about the next scene in their mystical story. "+\
            "Consider the current state of the adventure and the history of what has happened so far. Like any good DM, you let the hero make "+\
            "their own decisions in any conversations and other actions, you do not speak for the hero. However, don't let the hero perform unrealistic "+\
            "actions given thier character description. For instance, a knight typically cannot perform magic spells. "+\
            "The adventurer must follow your pace of the story. They are not allowed to fast-forward through events by dictating the story. "+\
            "You, the DM, control the story and will let the adventurers know if they attempt to take control of the unfolding events. "+\
            "If they have to walk through a forest to get to a location, they must go through the forest at your pace and deal "+\
            "with any encounters along the way to get there. They may not simply write 'I walked through the forest and arrived at the location'. "+\
            "They may not invent new characters or locations that did not previously exist unless you agree that they should be there. At the bottom, you find the latest input of the adventurers."
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
    

    def generateImage(self, state):
        instructions = "Generate a fantasy-style image accompanying the event in the scene below of a DnD adventure"
        scene = state.recent_history[-1][1]

        prompt = f"<instructions>\n{instructions}\n<\instructions>\n\n"+\
            f"<scene>\n{scene}\n</scene>"
        
        image = self.image_model.generate_images(
            prompt=prompt,
            number_of_images=1,
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
            aspect_ratio="3:4",
            negative_prompt="Outside",
        )

        return image
    

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
        self.inCombat = 0

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

