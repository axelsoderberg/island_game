# from region_class import Region
import random
import audio
import subprocess

#subprocess.call("keylogger/keylogger.py", shell=True)


'''import pygame
pygame.init()

size = width, height = 240, 135
screen = pygame.display.set_mode(size)
island = pygame.image.load("240x135.png")'''


class Region:
    def __init__(self, c, t, cords, i=0):
        self.climate = c
        self.texture = t
        self.location = cords
        self.item = i


def player_move(direction, player_region):  # Returns new region value for player
    if illegal_move(direction, player_region):  # Check for illegal move
        print("There's nothing but open water that way, try somewhere else!")
        sound.playSound("dialouge/nothing.wav")
        return player_region
    else:
        if direction == 1:
            player_region -= 3  # North
        if direction == 2:
            player_region -= 1  # West
        if direction == 3:
            player_region += 3  # South
        if direction == 4:
            player_region += 1  # East
        print("You start walking")
        sound.playSound("dialouge/walking.wav")
        return player_region


def illegal_move(direction, player_region):  # Check for illegal movement
    if player_region < 3 and direction == 1:  # Illegal move north
        return True
    if player_region % 3 == 0 and direction == 2:  # Illegal move west
        return True
    if player_region > 5 and direction == 3:  # Illegal move south
        return True
    if player_region > 5 and direction == 4:  # Illegal move east
        return True
    return False


def welcome():
    sound.playSoundtrack("audio/soundtrack/")
    print("Welcome player! You find yourself stranded at an unknown location, feel free to explore!")
    print("Please enter your name.")
    sound.playSound("dialouge/welcome.wav")
    name = input()
    return name


def request_player_action():
    while 1:
        sound.playSound("dialouge/action.wav", block=False)
        print("Choose an action: \n [1] Move north \n [2] Move west \n [3] Move south \n [4] Move east "
              "\n [5] Look around")
        action = input()
        if 0 < int(action) < 6:
            return int(action)
        else:

            print("Invalid input, please input a number from 1 to 5")
            sound.playSound("dialouge/invalid.wav")


def look(region, gold, shop_keeper):
    description = "You find yourself in a " + region.climate + ", "
    sound.queueSound("dialouge/yourself.wav")
    if region.climate == "cold":
        sound.queueSound("dialouge/cold.wav")
    elif region.climate == "fair":
        sound.queueSound("dialouge/fair.wav")
    elif region.climate == "warm":
        sound.queueSound("dialouge/warm.wav")

    if region.texture == "open":
        description += "open landscape. "
        sound.queueSound("dialouge/open.wav")
    elif region.texture == "forrest":
        description += 'green forrest. '
        sound.queueSound("dialouge/forest.wav")
    elif region.texture == "mountains":
        description += "region of mountains."
        sound.queueSound("dialouge/mountain.wav")
    print(description)
    sound.playQueue()

    if gold == 0 and region.item != 0:
        print("You also see something shimmering beneath some rocks; you find a bag of gold!")
        sound.playSound("dialouge/gold.wav")
        gold = 1
    if shop_keeper == region.location:
        print("Hey, there is another person here! He promises to get you home for a bag of gold")
        sound.playSound("dialouge/person.wav")
    return gold


regions = [Region("cold", "open", 0), Region("cold", "forrest", 1), Region("cold", "mountains", 2),
           Region("fair", "open", 3), Region("fair", "forrest", 4), Region("fair", "mountains", 5),
           Region("warm", "open", 6), Region("warm", "forrest", 7), Region("warm", "mountains", 8)]

currentRegion = 4
regions[random.randrange(0, 8)].item = "Bag of gold"
shopKeeperRegion = random.randrange(0, 8)
playerGold = 0

sound = audio.SoundEngine()
print("\n\n")
player_name = welcome()
print("Hello " + player_name)

while 1:
    # screen.blit(island)
    player_action = request_player_action()
    if int(player_action) < 5:
        currentRegion = player_move(player_action, regions[currentRegion].location)
        print(currentRegion)
    else:
        playerGold = look(regions[currentRegion], playerGold, shopKeeperRegion)
        if currentRegion == shopKeeperRegion and playerGold == 1:
            print("You hand over the bag of gold and the magic shopkeeper throws powder in the air and with colorful "
                  "sparks you escape the island. Congratulations " + player_name + "!")
            sound.playSound("dialouge/escape.wav")
            print("\n\nLead Programmer & Designer: Axel Söderberg\n"
                  "Audio & Programming: Tintin Axelsson\n"
                  "Voice Acting: Eric Ryberg")
            break
