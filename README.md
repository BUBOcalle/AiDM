# AiDM

To run the application, simply run Ai_DnD.py and enter the gradio hosted web interface at: http://127.0.0.1:7860. A suitable first message is "Begin the adventure!" after which the bot will act as a DM of a DnD adventure. 

Code structure: 
- Ai_DnD.py controls the flow of the chat interface and user interaction through gradio. 
- Ais.py contains all the code for the AI agents. 
- rollplayClasses.py contains code for defining all objects in the background process, as well as the fighting system logic. 
- combatTester.py is a simple script for testing combat. 
- EnemyExamples.py contains a few examples for few-shot learning, moved out of Ais.py for better readability. 

TODO (minor bug fixes we intend to fix before demo/presentation): 

Fix item/weapon update output format. Sometimes, the ai agent interpreting text to produce item update JSONs will make a mistake in the format of a new weapon. This should be fixed by adding examples for few-shot learning. 

Fix item/weapon update check for adventurer and not other characters. Sometimes, the same ai agent makes the mistake of assigning an item to the hero even though someone else in the story received it and not the hero. Could potentially be fixed by checking the prompt to make sure that it is clear who the llm should consider for item updates. 

