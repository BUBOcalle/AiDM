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
        return f"name: {self.name}, type: {self.type} location: {self.location}, description: {self.description}, battle skill: {self.battleSkill}."

class Enemy:
    def __init__(self, type: str, name: str, hp: int, battleSkill: int, location: str, description: str, damageOutput: int):
        self.type = type # player, enemy, npc
        self.name = name
        self.hp = hp
        self.battleSkill = battleSkill
        self.location = location
        self.description = description
        self.damageOutput = damageOutput

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
        heroHits = rollDice(hero.battleSkill)
        diff = enemyHits - heroHits
        if diff > 0:
            hero.hp -= enemy.damageOutput + diff
            update += f"\n{enemy.name} did {enemy.damageOutput + diff} damage to you!"
    return update

def heroAttackTurn(hero: Hero, enemy: Enemy, currentWeapon):
    update = f""
    heroHits = rollDice(hero.battleSkill)
    enemyHits = rollDice(enemy.battleSkill)
    diff = heroHits - enemyHits
    if diff > 0:
        enemy.hp -= currentWeapon.damage + diff
        update += f"\nYou did {currentWeapon.damage + diff} damage to {enemy.name}!"
    return update

class CombatScene:
    def __init__(self, hero: Hero, currentWeapon: Weapon, enemies: list[Enemy], starter):
        self.hero = hero
        self.currentWeapon = currentWeapon
        self.enemies = enemies
        self.turn = starter
    
    def combat(self):
        combatStillGoing = 1
        while combatStillGoing:
            update = f""
            if self.turn == "enemies":
                update += enemyTurn(self.hero, self.enemies)
                if self.hero.hp <= 0:
                    update += "\nYou died."
                    combatStillGoing = 0
            else:
                # check hero action
                heroAction = "attack" # get from input
                if heroAction == "attack":
                    target = Enemy() #from input
                    update += heroAttackTurn(self.hero, target, self.currentWeapon)
                    if target.hp <= 0:
                        self.enemies.remove(target)
                        update += f"\n{target.name} is dead."
                    if len(self.enemies) == 0:
                        update += "\nYou have killed all the enemies. The battle is won!"
                        combatStillGoing = 0
                else:
                    allowedToFlee = 1 # get from ai # StoryTeller asks where you want to flee and if it makes sense it lets you
                    if allowedToFlee:
                        update += "\nYou flee the scene" 
                        combatStillGoing = 0
                    else:
                        update += "\nYou look around for a flight path but can't find one and waste your turn."
            if self.turn == "enemies":
                self.turn = "hero"
            else:
                self.turn = "enemies"
            # send update to storyTeller
        # Notify storyTeller of end of combat scene

    
