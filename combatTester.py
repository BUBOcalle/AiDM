from rollplayClasses import *

hero = Hero(type="hero", name="Calle Dachalin", hp=15, battleSkill=12, location="the tavern", description="a tall blonde man with a destiny", equipment=["his favourite book", "flint and steel", "some beer"], weapons=[Weapon(3, "Mighty stick")])
enemyNames = ["goblin1", "goblin2", "goblin3"]
enemies = []
for name in enemyNames:
    enemies.append(Enemy("enemy", name, 7, 6, "", "", 1))

combatScene = CombatScene(hero, hero.weapons[0], enemies, "hero")

combatScene.combat()