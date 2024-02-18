import random

sword_lv1=10
sword_lv1_durability=10
shield_lv1=100
health=100
armor=100
difficulty=1
inventory=['Health Potion', 'Strength Potion']
loot=['Health Potion','Strength Potion','Sword','Shield']
strength=100
score=0
monster_chance_lv1=4/difficulty
monster_health=100*difficulty
crit_level=5
strength_level=1*difficulty
strength_bonus=1
strength_time=0

user_name = input("Enter your name: ")
valid_difficulty_levels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
while True:
    difficulty = input('Enter your difficulty level (1-10): ')
    if difficulty in valid_difficulty_levels:
        difficulty = int(difficulty)
        break
    else:
        print("Invalid input. Please enter a valid difficulty level.")
print(f'Hello, {user_name}! Welcome to my game. Your difficulty level is: {difficulty}\nRemember to type all answers in lowercase.\n')
print(f'Your current health is: {health}\nYour current armor durability is: {armor}\nIn your inventory, there is: {inventory}\n')

def potion_take():
    global potion,health,inventory,strength,difficulty,strength_bonus,strength_level,strength_time
    while True:
        answer = input('What type of potion do you want to take? (Health, Strength): ').lower()
        if answer == 'health':
            if 'Health Potion' in inventory:
                potion = random.randint(20, 100) * difficulty
                health += potion
                print(f'\nThe potion healed: {potion} health\n')
                inventory.remove('Health Potion')
                break
            else:
                print("You don't have any health potions.")
        elif answer == 'strength':
            if 'Strength Potion' in inventory:
                strength = random.randint(2, 5) * difficulty
                strength_bonus = strength + strength_level
                strength_time = 5
                print(f'\nThe potion increased your strength bonus to: {strength_bonus} and it will last for 5 attacks.\n')
                inventory.remove('Strength Potion')
                break
            else:
                print("You don't have any strength potions.")
        else:
            print("Invalid choice. Please select 'Health' or 'Strength'.")

def monster_hunt():
    global health,armor,difficulty,inventory,loot,strength,score,shield_lv1,monster_health,sword_lv1_durability,sword_lv1,strength_level,strength_time,strength_bonus
    damage_dealt=random.randint(sword_lv1,(sword_lv1*crit_level))*strength_bonus
    monster_health=(monster_health-damage_dealt)
    durability_loss=random.randint(1,2)
    sword_lv1_durability=(sword_lv1_durability-durability_loss)
    print('You used your sword and dealt',damage_dealt,"damage to the monster it's health is now",monster_health,"your sword took",durability_loss,"durability loss and it's durability is now",sword_lv1_durability)
    if strength_time >= 1:
        strength_time-=1
    if strength_time <= 0:
        strength_bonus = 0
    if sword_lv1_durability <= 0:
        print("Your sword broke")
        inventory.remove('Sword')
    if monster_health >= 1:
        monster_attack()
    else:
        score += 1
        print('You defeated the monster and your score incresed by 1, it is now:', score)

def monster_attack():
    global health,armor,difficulty,inventory,loot,strength,score,shield_lv1,monster_health,sword_lv1_durability,sword_lv1,strength_level,strength_time
    monster_hit=int(random.randint(1,50)*difficulty)
    if 'Shield' in inventory:
        shield_lv1=int(shield_lv1-monster_hit)
        print("You have been hit by a monster for",monster_hit,"points your sheild took the full hit and it's durability is now:",shield_lv1,'\n')
        if shield_lv1 <= 0:
            print("Your shield broke")
            inventory.remove('Shield')
        if 'Sword' in inventory:
            answer=input('You have a sword in your inventory do you use it on the monster? ')
            if answer == (f'yes') or (f'y'):
                monster_hunt()  
    else:
        health=int(health-(monster_hit/3))
        armor=int(armor-((monster_hit/3)*2))
        print("You have been hit by a monster for",monster_hit,"points")
        print("\nAfter being hit your health has dropped down to:",health,"points and your armor has dropped to:",armor)
        if 'Sword' in inventory:
            answer=input('You have a sword in your inventory do you use it on the monster? ')
            if answer == (f'yes') or (f'y'):
                monster_hunt()
        else:
            print("You don't havee a sword to attack with so you can't fight back")

    if monster_health <= 0 and health>=1:
        print('You have survived the attack, lets keep going\n')
        monster_health=100*difficulty
    elif health <= 0:
        print('You have died your score is:',score)
        exit

    if 'Health Potion' in inventory:
        potion_accept = input('would you like to take a health potion? (yes,no) ')
        if potion_accept == "yes" or potion_accept == "y":
            potion=int(random.randint(20,100)*difficulty)
            health=health+potion
            print('\nThe potion healed:',potion,'health\n')
            inventory.remove('Health Potion')
        else:
            print('You choose not to take the potion you health remains unchsnged')
    print('Your current helath is:',health,'\nYour current armor durability is:',armor,'\nIn your inventory there is:',inventory,'\n')

while True:
    if random.randint(1,monster_chance_lv1) == 1:
        monster_attack()
    else:
        answer = input('You were not attacked by a monster, what do you do? (loot, potion, hunt) ')
        if answer.lower() == 'loot':
            if not loot:
                if 'Sword' in inventory:
                    answer=input('There is no loot around you, do you hunt a monster? ')
                    if answer.lower() == 'yes' or 'y':
                        monster_attack()
                else:
                    print('There is no loot around you and you have no sword to hunt monsters with')
            else:
                new_loot = random.choice(loot)
                inventory.append(new_loot)
                loot.remove(new_loot)
                print(f"You found {new_loot} and added it to your inventory.\n")
                print('Now in your inventory there is:',inventory,'\n')
        elif answer.lower() == 'potion':
            potion_take()
        elif answer.lower() == 'hunt':
            monster_hunt()
        else:
            print("You can't do that")