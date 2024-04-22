import random
import json
import requests

shield_lv1=100
difficulty=1
inventory=['Health Potion', 'Strength Potion']
loot=['Health Potion','Strength Potion','Sword','Shield']
score=0
monster_chance_lv1=4/difficulty
monster_health=100*difficulty
crit_level=5

player={
    "health": 100,
    "armor": 100,
    "strength": 100
}
strength_potion={
    "potancy": 100,
    "duration": 5
}
health_potion={
    "strength":100,
    "bonus":1
}
sword={
    "damage": 10,
    "durability": 10
}

valid_difficulty_levels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
done=False

value = requests.get('https://dweet.io/get/latest/dweet/for/text-based-terminal-game-highscore')
prev_score = value.json()
try:
    print("The previous high score is:", prev_score['with'][0]['content']['value'], "\n")
except:
    print("Error retrieving previous high score\n")
    print("The returned values were: ", value)

while done!=True:
    difficulty = input('\nEnter your difficulty level (1-10): ')
    try:
        difficulty = int(difficulty)
        placeholder=player['strength']*difficulty
        player.update({'strength':placeholder})
        break
    except:
        print("Invalid input. Please enter a valid difficulty level.")

print(f'Your difficulty level is: {difficulty}\n\nRemember to type all answers in lowercase. You can also stop the game by typing stop or exit.\n\nYour current health is: {player["health"]}\nYour current armor durability is: {player["armor"]}\nYour current strength is: {player["strength"]}\nIn your inventory, there is: {inventory}\n')

def potion_take():
    global potion,inventory,difficulty,strength_time
    while True:
        answer = input(f'What type of potion do you want to take? (Health, Strength, None) Your have {inventory} in your inventory: ').lower()
        if answer == 'health':
            if 'Health Potion' in inventory:
                potion = random.randint(20, 100) * difficulty
                player["health"] += potion
                print(f'\nThe potion healed: {potion} health\n')
                inventory.remove('Health Potion')
                break
            else:
                print("You don't have any health potions.")
        elif answer == 'strength':
            if 'Strength Potion' in inventory:
                bonus = int(random.randint(2,5)) * int(difficulty) + int(strength_potion["potancy"])
                player.update({"strength":bonus})
                strength_time = 5
                print(f'\nThe potion increased your strength bonus to: {player["strength"]} and it will last for 5 attacks.\n')
                inventory.remove('Strength Potion')
                break
            else:
                print("You don't have any strength potions.")
        elif answer.lower() == 'none' or 'n':
            print("You changed you mind and took no potions\n")
            break
        else:
            print("Invalid choice. Please select 'Health', 'Strength' or 'None'.")

def monster_hunt():
    global player,difficulty,inventory,loot,score,shield_lv1,monster_health,sword,strength_time
    damage_dealt=random.randint(sword['damage'],(sword['damage']*crit_level))
    monster_health=(monster_health-damage_dealt)
    durability_loss=random.randint(1,2)
    sword['durability']=(sword['durability']-durability_loss)
    print('You used your sword and dealt',damage_dealt,"damage to the monster it's health is now",monster_health,"your sword took",durability_loss,"durability loss and it's durability is now",sword['durability'])
    if strength_potion['duration'] >= 1:
        strength_potion['duration']-=1
    if strength_potion['duration'] <= 0:
        strength_potion['duration'] = 5
        player['strength']-=strength_potion['potancy']
    if sword['durability'] <= 0:
        print("Your sword broke")
        if 'Sword' in inventory:
            inventory.remove('Sword')
    if monster_health >= 1:
        monster_attack()
    else:
        score += 1
        print('You defeated the monster and your score incresed by 1, it is now:', score)

def monster_attack():
    global player,difficulty,inventory,loot,score,shield_lv1,monster_health,sword,strength_time
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
            elif answer.lower() == 'no' or 'n':
                print("Your didn't use your sword...\n")
    else:
        player['health']=int(player["health"]-(monster_hit/3))
        player["armor"]=int(player["armor"]-((monster_hit/3)*2))
        print("You have been hit by a monster for",monster_hit,"points")
        print("\nAfter being hit your health has dropped down to:",player["health"],"points and your armor has dropped to:",player["armor"])
        if 'Sword' in inventory:
            answer=input('You have a sword in your inventory do you use it on the monster? ')
            if answer == (f'yes') or (f'y'):
                monster_hunt()
            elif answer.lower() == 'no' or 'n':
                print("Your didn't use your sword...\n")
        else:
            print("You don't havee a sword to attack with so you can't fight back")

    if monster_health <= 0 and player["health"]>=1:
        print('You have survived the attack, lets keep going\n')
        monster_health=100*difficulty
    elif player["health"] <= 0:
        print('You have died your score is:',score)
        requests.post('https://dweet.io/dweet/for/text-based-terminal-game-highscore?', data={'value':score})
        exit

    if 'Health Potion' in inventory:
        potion_accept = input('would you like to take a health potion? (yes,no) ')
        if potion_accept == "yes" or potion_accept == "y":
            potion=int(random.randint(20,100)*difficulty)
            player["health"]=player['health']+potion
            print('\nThe potion healed:',potion,'health\n')
            inventory.remove('Health Potion')
        else:
            print('You choose not to take the potion you health remains unchsnged')
    print('Your current helath is:',player['health'],'\nYour current armor durability is:',player['armor'],'\nIn your inventory there is:',inventory,'\n')

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
        elif answer.lower() == 'exit' or 'stop':
            print('You have ended your own life...\nYour score is:',score)
            try:
                requests.post('https://dweet.io/dweet/for/text-based-terminal-game-highscore?', data={'value':score})
                print('\nHighscore has been updated')
            except:
                print("Error updating high score")
            exit()
        else:
            print("You can't do that")
