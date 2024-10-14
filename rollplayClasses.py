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
        self.hp = array[1]
        self.battleSkill = array[2]
        self.damageOutput = array[3]

    def __str__(self):
        return f"name: {self.name}, type: {self.type} location: {self.location}, description: {self.description}, battle skill: {self.battleSkill}, damage output: {self.damageOutput}."

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
    
    def combat(self):
        combatStillGoing = 1
        print(f"Combat has started. {self.hero.name} is facing:")
        for enemy in self.enemies:
            print(enemy.name)
        while combatStillGoing:
            update = f""
            if self.turn == "enemies":
                print(f"It's the enemies' turn!")
                update += enemyTurn(self.hero, self.enemies)
                if self.hero.hp <= 0:
                    update += "\nYou died."
                    combatStillGoing = 0
            else:
                print(f"It's your turn!")
                while True:
                    heroAction = input("Would you like to attack someone or flee?\n")
                    actionCommand = heroAction.split(" ")
                    if actionCommand[0] == "attack":
                        targetName = actionCommand[1]
                        target = 0
                        for enemy in self.enemies:
                            if enemy.name == targetName:
                                target = enemy
                                break
                        if target == 0:
                            print(f"There is no enemy called {targetName}. Try again!")
                        else:
                            update += heroAttackTurn(self.hero, target, self.currentWeapon)
                            if target.hp <= 0:
                                self.enemies.remove(target)
                                update += f"\n{target.name} is dead."
                            if len(self.enemies) == 0:
                                update += "\nYou have killed all the enemies. The battle is won!"
                                combatStillGoing = 0
                            break
                    elif actionCommand[0] == "flee":
                        allowedToFlee = 1 # get from ai # StoryTeller asks where you want to flee and if it makes sense it lets you
                        if allowedToFlee:
                            update += "\nYou flee the scene" 
                            combatStillGoing = 0
                        else:
                            update += "\nYou look around for a flight path but can't find one and waste your turn."
                        break
                    else:
                        print("You have not formatted your command correctly. Write either:\nattack [enemy]\nor\nflee")
            if self.turn == "enemies":
                self.turn = "hero"
            else:
                self.turn = "enemies"
            print(update)
        print("Combat has ended <3")

    
