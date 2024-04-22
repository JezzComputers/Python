import random

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_item(self, item):
        self.items.append(item)

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def remove_item_from_inventory(self, item):
        self.inventory.remove(item)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

def create_game():
    # Create rooms
    kitchen = Room("Kitchen", "A room with a large table and some cooking utensils.")
    bedroom = Room("Bedroom", "A cozy bedroom with a comfortable bed.")
    garden = Room("Garden", "A beautiful garden with colorful flowers.")
    attic = Room("Attic", "A dusty attic filled with old furniture.")

    # Connect rooms
    kitchen.add_exit("north", bedroom)
    kitchen.add_exit("east", garden)
    bedroom.add_exit("south", kitchen)
    garden.add_exit("west", kitchen)
    bedroom.add_exit("up", attic)
    attic.add_exit("down", bedroom)

    # Create items
    key = Item("Key", "A rusty old key.")
    sword = Item("Sword", "A sharp sword.")
    flower = Item("Flower", "A beautiful red flower.")

    # Add items to rooms
    kitchen.add_item(key)
    bedroom.add_item(sword)
    garden.add_item(flower)

    # Create player
    player_name = input("Enter your name: ")
    player = Player(player_name)

    return player, kitchen

def main():
    player, current_room = create_game()
    print(f"Welcome, {player.name}, to the text-based adventure game!")

    while True:
        print("\n--- Current Location ---")
        print(f"{current_room.name}: {current_room.description}")

        # Display available exits
        print("Exits:", ", ".join(current_room.exits.keys()))

        # Display items in the room
        if current_room.items:
            print("Items in the room:", ", ".join(item.name for item in current_room.items))

        # Display player inventory
        if player.inventory:
            print("Your Inventory:", ", ".join(item.name for item in player.inventory))

        # Get player input
        action = input("What do you want to do? ").strip().lower()

        # Handle movement
        if action in current_room.exits:
            current_room = current_room.exits[action]
        else:
            print("Invalid action. Try again.")

        # Handle picking up items
        if action.startswith("pick up "):
            item_name = action[8:]
            for item in current_room.items:
                if item.name.lower() == item_name:
                    player.add_item_to_inventory(item)
                    current_room.items.remove(item)
                    print(f"You picked up {item.name}.")
                    break
            else:
                print("Item not found in this room.")

        # Handle dropping items
        if action.startswith("drop "):
            item_name = action[5:]
            for item in player.inventory:
                if item.name.lower() == item_name:
                    player.remove_item_from_inventory(item)
                    current_room.add_item(item)
                    print(f"You dropped {item.name}.")
                    break
            else:
                print("Item not found in your inventory.")

        # Check for game completion condition
        if current_room.name == "Attic" and "key" in [item.name.lower() for item in player.inventory]:
            print("Congratulations! You found the key and completed the game.")
            break

if __name__ == "__main__":
    main()
