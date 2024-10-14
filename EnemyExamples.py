from rollplayClasses import Enemy

EXAMPLES = [
    'name/title:Thief, hp:12, battleSkill:10, damageOutput:3', 
    'name/title:Bear, hp:20, battleSkill:10, damageOutput:5',
    'name/title:Goblin, hp:7, battleSkill:5, damageOutput:2',
    'name/title:Dragon, hp:100, battleSkill:30, damageOutput:8',
    'name/title:Knight, hp:15, battleSkill:12, damageOutput:4'
]

if __name__ == "__main__":
    examples = ""
    for example in EXAMPLES:
        examples +=  example + "\n"
    enemies = []
    for line in examples[:-1].split("\n"):
        attributes = [a.split(":")[1] for a in line.split(",")]
        enemies.append(Enemy(attributes))
    print(enemies)