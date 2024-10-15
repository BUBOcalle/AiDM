from rollplayClasses import Enemy

EXAMPLES = [
    '{\nenemies: \n[\n{\nname:Thief, \nhp:12, \nbattleSkill:10, \ndamageOutput:3\n},\n', 
    '{\nname:Bear, \nhp:20, \nbattleSkill:10, \ndamageOutput:5\n},\n',
    '{\nname:Goblin, \nhp:7, \nbattleSkill:5, \ndamageOutput:2\n},\n',
    '{\nname:Dragon, \nhp:100, \nbattleSkill:30, \ndamageOutput:8\n},\n',
    '{\nname:Knight, \nhp:15, \nbattleSkill:12, \ndamageOutput:4\n]\n}\n'
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