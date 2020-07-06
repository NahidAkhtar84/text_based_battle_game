from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random



#create Black Magic
fire = Spell("Fire", 20, 600, "black")
thunder = Spell("Thunder", 22, 620, "black")
blizzard = Spell("Blizzard", 23, 730, "black")
meteor = Spell("Meteor", 30, 800, "black")
quake = Spell("Quake", 25, 750, "black")

#create White spell
cure = Spell("Cure", 22, 620, "white")
cura = Spell("Cura", 34, 1200, "white")

#create some items
potion = Item("Potion", "potion", "Heals 50 HP", 500)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 1000)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 2000)
elixer = Item("Elixer", "elixer", "Fully Restore HP/HP of one party member", 9999)
megaelixer = Item("MegaElixer", "elixer", "Fully Restore HP/HP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
player_item = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
               {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
               {"item": megaelixer, "quantity": 2}, {"item": grenade, "quantity": 5}]
#Instantiate people
player1 = Person("Valos :", 3460, 165, 290, 34, player_magic , player_item)
player2 = Person("Kudduc:", 4160, 185, 320, 34, player_magic , player_item)
player3 = Person("Siggy :", 3960, 145, 360, 34, player_magic , player_item)

enemy1 = Person("Jergon:  ", 1569, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Shereder:", 18200, 705, 545, 25, enemy_spells, [])
enemy3 = Person("Komada:  ", 1269, 230, 570, 225, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i=0

while running:

    print("======================================================")
    print("\n\n")
    print("NAME                    HP                                    MP")

    #If action is selected
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()
    print("\n")

    for player in players:
        player.choose_action()
        choice = input("Choose Action >>> ")
        index = int(choice)-1

        if index == 0:
            dmg = player.damage_generate()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You Attacked for "+ enemies[enemy].name , dmg, " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died!")
                del enemies[enemy]
        #If Magic is selected
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic >>> ")) - 1

            if magic_choice == -1:
                continue
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not Enough MP, Your spell Did not work!\n" + bcolors.ENDC)
                continue
            # Reduce the player mp
            player.reduce_mp(spell.cost)
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), "HP! \n" + bcolors.ENDC)
            elif spell.type == "black":
            #Damage the enemy if the spell works
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals to " + enemies[enemy].name , str(magic_dmg), "points of damage!\n" + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died!")
                    del enemies[enemy]


        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "None Left...." + bcolors.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP and MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + "deals to" + enemies[enemy].name , str(item.prop), "points of Damage!" + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died!")
                    del enemies[enemy]

#Ending the game
    print("*******************")
    print(len(players))
    print(len(enemies))
    print("*******************")
    if len(players) == 0:
        print(bcolors.FAIL + "Your Enemies have defeated You!" + bcolors.ENDC)
        running = False

    if len(enemies) == 0:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False


#Enemy attacks
    print(bcolors.FAIL +bcolors.BOLD + "Enemy Attacks!"+ bcolors.ENDC)
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.damage_generate()

            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + bcolors.BOLD+enemy.name.replace(" ", "") + "Attacked" + players[target].name.replace(" ", "") + "for ", enemy_dmg, " points of damage." + bcolors.ENDC)


        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            #print("Enemy choose ", spell.name, " damage is ", magic_dmg)


            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + "\n" + spell.name + " heals" + enemy.name + "for ", str(magic_dmg), "HP! \n" + bcolors.ENDC)
            elif spell.type == "black":
            #Damage the enemy if the spell works
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + "\n" + enemy.name.replace(" ", "") + " causes to " + players[target].name , str(magic_dmg), "points of damage by" + spell.name +"\n" + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died!")
                    del players[target]



