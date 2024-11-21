import random
import time

class Player:
    def __init__(self):
        self.health = 100
        self.ammo = 5
        self.inventory = {'food': 2}  # Initial inventory with 2 food items
        self.money = 50  # Player starts with 50 money
        self.alive = True
        self.weapon = 'pistol'  # Default weapon is a pistol
        self.weapon_ammo = 5  # Ammo for pistol (5 bullets)
        self.money_found = 0  # Money earned from animals
        self.kills = 0  # Keep track of how many animals the player has killed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def heal(self):
        if 'food' in self.inventory and self.inventory['food'] > 0:
            self.health += 30  # Food restores 30 health
            self.inventory['food'] -= 1
            print("You ate food and healed 30 health!")
        else:
            print("You don't have any food!")
    
    def buy_item(self, item, cost):
        if self.money >= cost:
            self.money -= cost
            if item == 'ammo':
                self.ammo += 5
            elif item == 'food':
                self.inventory['food'] += 1
            elif item == 'm60':
                self.weapon = 'm60'  # Switch to M60 when bought
                self.weapon_ammo = 500  # M60 starts with 500 bullets
                print("You bought the M60 machine gun!")
            elif item == 'semi_auto_rifle':
                self.weapon = 'semi_auto_rifle'  # Switch to SemiAutoRifle when found
                self.weapon_ammo = 100  # SemiAutoRifle starts with 100 bullets
                print("You picked up the Semi-Auto Rifle with 100 rounds!")
            print(f"Purchased {item} for {cost} money.")
        else:
            print("Not enough money!")
    
    def is_alive(self):
        return self.alive


class Animal:
    def __init__(self, name, tier, money_reward, health, damage):
        self.name = name
        self.tier = tier
        self.money_reward = money_reward
        self.health = health
        self.attack_damage = damage
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"You defeated the {self.name}!")
            return True
        return False
    
    def attack(self):
        return self.attack_damage

    def get_money_reward(self):
        return self.money_reward


class M60:
    def __init__(self):
        self.damage_per_bullet = 25
        self.accuracy = 50  # 50% chance to hit
        self.bullets_per_shot = 20
        self.ammo = 500  # M60 starts with 500 bullets
    
    def shoot(self, player, animal):
        if self.ammo < self.bullets_per_shot:
            print("Not enough ammo for a full burst! Visit the shop to buy more.")
            return False
        
        self.ammo -= self.bullets_per_shot
        print("Firing the M60...")
        time.sleep(1)
        
        total_damage = 0
        for _ in range(self.bullets_per_shot):
            if random.randint(1, 100) <= self.accuracy:  # 50% chance to hit each bullet
                total_damage += self.damage_per_bullet
        print(f"You hit the {animal.name} for {total_damage} total damage with the M60!")
        return animal.take_damage(total_damage)


class SemiAutoRifle:
    def __init__(self):
        self.damage_per_bullet = 20
        self.accuracy = 70  # 70% chance to hit
        self.ammo = 100  # SemiAutoRifle starts with 100 bullets
    
    def shoot(self, player, animal):
        if self.ammo <= 0:
            print("Out of ammo for the Semi-Auto Rifle! Visit the shop to buy more.")
            return False
        
        self.ammo -= 1
        print("Firing the Semi-Auto Rifle... BANG!")
        time.sleep(1)

        # Check for hit accuracy
        if random.randint(1, 100) <= self.accuracy:  # 70% chance to hit
            total_damage = self.damage_per_bullet
            print(f"You hit the {animal.name} for {total_damage} damage with the Semi-Auto Rifle!")
            animal.take_damage(total_damage)
        else:
            print("You missed!")
        
        # ASCII art for trees falling after each shot
        print("\nTree falls with each shot...")
        self._falling_tree_animation()

        return True

    def _falling_tree_animation(self):
        trees = [
            "   ||  ",
            "   ||  ",
            "   ||  ",
            "   ||  ",
            "   ||  ",
            "   ||  ",
            "  /||\\ ",
            "   ||  ",
            "   ||  ",
            "   ||  "
        ]
        for i in range(len(trees)):
            print(trees[i])
            time.sleep(0.1)


def shoot(player, animal):
    print(f"Attempting to shoot the {animal.name} with {player.weapon}...")
    if player.weapon == 'pistol':
        if player.ammo <= 0:
            print("Out of ammo! Visit the shop to buy more.")
            return False

        player.ammo -= 1
        print("Aiming at the animal...")
        time.sleep(1)

        chance_to_hit = random.randint(1, 100)

        # 75% chance to hit the animal, 25% chance to miss
        if chance_to_hit <= 75:
            damage = random.randint(10, 25)  # Random damage between 10 and 25
            print(f"You hit the {animal.name} for {damage} damage!")
            return animal.take_damage(damage)
        else:
            print(f"You missed the {animal.name}!")
            return False
    elif player.weapon == 'm60':  # M60 shooting
        m60 = M60()
        return m60.shoot(player, animal)
    elif player.weapon == 'semi_auto_rifle':  # Semi-Auto Rifle shooting
        semi_auto_rifle = SemiAutoRifle()
        return semi_auto_rifle.shoot(player, animal)


def bear_turn(player, animal):
    print(f"The {animal.name} attacks!")
    damage = animal.attack()
    player.take_damage(damage)
    print(f"The {animal.name} dealt {damage} damage to you.")

def show_status(player):
    print(f"\nPlayer Health: {player.health} | Ammo: {player.ammo} | Money: {player.money}")
    print(f"Food: {player.inventory.get('food', 0)} | Weapon: {player.weapon} ({player.weapon_ammo} ammo)")

def shop(player):
    print("\nWelcome to the Shop!")
    print("1. Buy Ammo (5 bullets) - 20 money")
    print("2. Buy Food (heals 30 health) - 15 money")
    print("3. Buy M60 Machine Gun (500 ammo) - 200 money")
    print("4. Exit Shop")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        player.buy_item('ammo', 20)
    elif choice == "2":
        player.buy_item('food', 15)
    elif choice == "3":
        player.buy_item('m60', 200)
    elif choice == "4":
        print("Exiting the shop.")
        return
    else:
        print("Invalid choice. Try again.")
    time.sleep(1)

def encounter_animal(player):
    # Randomly select an animal encounter
    animals = [
        Animal('Deer', 'Tier 1', 10, 30, 5),
        Animal('Raccoon', 'Tier 1', 15, 20, 4),
        Animal('Coyote', 'Tier 2', 25, 40, 7),
        Animal('Bear', 'Tier 3', 50, 50, 15),
        Animal('Moose', 'Tier 3', 60, 70, 20),
        Animal('Bird', 'Tier 1', 5, 10, 2)
    ]

    animal = random.choice(animals)
    print(f"\nA wild {animal.name} appears!")
    return animal

def game_loop():
    print("Game script is running...")  # Added print statement for debugging
    player = Player()

    # Ask the player if they want to pick up the Semi-Auto Rifle
    print("You find a Semi-Auto Rifle with 100 rounds of ammo. Do you want to pick it up?")
    choice = input("Enter 'yes' to pick up the Semi-Auto Rifle or 'no' to leave it: ").lower()
    if choice == 'yes':
        player.weapon = 'semi_auto_rifle'
        player.weapon_ammo = 100
        print("You have picked up the Semi-Auto Rifle.")

    while player.is_alive():
        show_status(player)

        # Random encounter in the woods
        print("\nWalking through the forest...")
        time.sleep(2)

        print("Trees slowly sway as you walk through the forest...")
        print("A little character walks into view...\n")
        print("       O  ")
        print("      /|\\ ")
        print("      / \\  ")
        print("You encounter an animal!")
        
        animal = encounter_animal(player)
        time.sleep(1)

        # Player encounters animal, battle begins
        if shoot(player, animal):
            player.money += animal.get_money_reward()
            print(f"You earned {animal.get_money_reward()} money!")
            print(f"Current Money: {player.money}")
            player.kills += 1

        else:
            bear_turn(player, animal)

        # After killing 3 animals, ask the player if they want to buy anything or leave
        if player.kills >= 3:
            print("You've killed 3 animals.")
            print("Would you like to buy anything? (yes/no)")
            buy_choice = input().lower()
            if buy_choice == 'yes':
                shop(player)
            else:
                print("Do you want to leave the forest? (yes/no)")
                leave_choice = input().lower()
                if leave_choice == 'yes':
                    print("You leave the forest.")
                    break

    print("Game Over! You died.")

game_loop()
