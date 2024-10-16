import random

class Weapon:
    def __init__(self, damage: int, name):
        self.name = name
        self.damage = damage
    
    def __str__(self):
        return f"name: {self.name}, damage: {self.damage}"
    
class Hero:
    def __init__(self, type: str, name: str, hp: int, battleSkill: int, location: str, description: str, equipment: list[str], weapons: list[Weapon]):
        self.type = type # player, enemy, npc
        self.name = name
        self.hp = hp
        self.battleSkill = battleSkill
        self.location = location
        self.description = description
        self.equipment = equipment
        self.weapons = weapons

    def __str__(self):
        return f"name: {self.name}, type: {self.type} location: {self.location}, description: {self.description}, "+\
            f"battle skill: {self.battleSkill}, equipment: {[item for item in self.equipment]}, weapons: {[str(weapon) for weapon in self.weapons]}."

class Enemy:
    def __init__(self, type: str, name: str, hp: int, battleSkill: int, location: str, description: str, damageOutput: int):
        # self.type = type # player, enemy, npc
        self.name = name
        self.hp = hp
        self.battleSkill = battleSkill
        # self.location = location
        # self.description = description
        self.damageOutput = damageOutput

    def __init__(self, array):
        self.name = array[0]
        self.hp = int(array[1])
        self.battleSkill = int(array[2])
        self.damageOutput = int(array[3])

    def __str__(self):
        return f"name: {self.name}, hp:{self.hp}, battle skill: {self.battleSkill}, damage output: {self.damageOutput}."

class npc:
    def __init__(self, name: str, description: str, location: str):
        self.name = name
        self.description = description
        self.location = location


    def __str__(self):
        return f"name: {self.name}, type: {self.type} location: {self.location}, description: {self.description}."
    
def rollDice(n):
    result = 0
    for _ in range(n):
        if random.randint(1,6) == 6:
            result += 1
    return result

def enemyTurn(hero: Hero, enemies: list[Enemy]):
    update = f""
    for enemy in enemies:
        enemyHits = rollDice(enemy.battleSkill)
        #print(f"{enemy.name} got {enemyHits} hits.")
        heroHits = rollDice(hero.battleSkill)
        #print(f"{hero.name} got {heroHits} hits.")
        diff = enemyHits - heroHits
        if diff > 0:
            hero.hp -= enemy.damageOutput + diff
            update += f"\n{enemy.name} did {enemy.damageOutput + diff} damage to {hero.name}, who now has {hero.hp} hp!"
        else:
            update+=f"\n{enemy.name} tries to attack {hero.name}, but misses!"
    return update

def heroAttackTurn(hero: Hero, enemy: Enemy, currentWeapon):
    update = f""
    heroHits = rollDice(hero.battleSkill)
    #print(f"{hero.name} got {heroHits} hits.")
    enemyHits = rollDice(enemy.battleSkill)
    #print(f"{enemy.name} got {enemyHits} hits.")
    diff = heroHits - enemyHits
    if diff > 0:
        enemy.hp -= currentWeapon.damage + diff
        update += f"\n{hero.name} did {currentWeapon.damage + diff} damage to {enemy.name}!"
    else:
        update += f"\n{hero.name} tries to attack {enemy.name}, but misses!"
    return update

class CombatScene:
    def __init__(self, hero: Hero, currentWeapon: Weapon, enemies: list[Enemy], starter):
        self.hero = hero
        self.currentWeapon = currentWeapon
        self.enemies = enemies
        self.turn = starter

    def __init__(self):
        self.combatState = "default"
    

    
    def combatStart(self):
        output = ""
        output += f"Combat has started! \n\n{self.hero.name} is facing:\n"
        for enemy in self.enemies:
            output += enemy.name
            output += "\n"
        output += f"\nIt's your turn!\n"
        output += "\nWould you like to attack someone or flee?\n"
        return output
    
    def inCombat(self, input):
        update = ""
        actionCommand = input
        print(actionCommand)
        #HERO TURN
        if "attack" in actionCommand:
            actionCommand = actionCommand.split("attack ")
            print(actionCommand)
            if(len(actionCommand) > 1 and actionCommand[1] in [enemy.name for enemy in self.enemies]):
                targetName = actionCommand[1]
                for enemy in self.enemies:
                    if enemy.name == targetName:
                        target = enemy
                        break

                update += heroAttackTurn(self.hero, target, self.currentWeapon)
                if target.hp <= 0:
                    self.enemies.remove(target)
                    update += f"\n{target.name} is dead."
                if len(self.enemies) == 0:
                    update += "\nYou have killed all the enemies. The battle is won!\nWhat do you do?"
                    return update, 0, 0
            else:
                if(len(actionCommand) == 1 or len(actionCommand[1]) < 2):
                    self.combatState = "targetChoose"
                    return "Who do you want to attack?", 1, -1
                else:
                    self.combatState = "targetChoose"
                    return "that enemy is not in the list of enemies, who do you want to attack?", 1, -1
        elif "flee" in actionCommand:
            allowedToFlee = 1 # get from ai # StoryTeller asks where you want to flee and if it makes sense it lets you
            if allowedToFlee:
                update += "\nYou flee the scene!\nWhat do you do?" 
                return update, 0, 1
            else:
                update += "\nYou look around for a flight path but can't find one and waste your turn."
        else:
            return "You have not formatted your command correctly. Write either:\nattack [enemy]\nor\nflee", 1, -1
            
        #ENEMY TURN  
        update += f"\nIt's the enemies' turn!\n"
        update += enemyTurn(self.hero, self.enemies)
        if self.hero.hp <= 0:
            update += "\nYou died. :("
            return update, 0, 2

        return update, 1, -1
        
    

    def curentCombatState(self, input):
        if self.combatState == "default":
            return self.inCombat(input)
        if self.combatState == "targetChoose":
            self.combatState = "default"
            return self.inCombat("attack " + input)

        return "WTF combatstate error", 1
