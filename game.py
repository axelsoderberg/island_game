import pygame as pg
import random
import audio
import draw
import subprocess

# subprocess.call("keylogger/keylogger.py", shell=True)


pg.init()
clock = pg.time.Clock()
sound = audio.SoundEngine()


class Player:
    def __init__(self):
        self.name = ""
        self.region = 4
        self.region_shop_keeper = random.randrange(0, 8)
        self.gold = 0


class Region:
    def __init__(self, c, t, cords, i=0):
        self.climate = c
        self.texture = t
        self.location = cords
        self.item = i


regions = [Region("cold", "open", 0), Region("cold", "forrest", 1), Region("cold", "mountains", 2),
           Region("fair", "open", 3), Region("fair", "forrest", 4), Region("fair", "mountains", 5),
           Region("warm", "open", 6), Region("warm", "forrest", 7), Region("warm", "mountains", 8)]
regions[random.randrange(0, 8)].item = "Bag of gold"


def player_move(direction, player):  # Returns new region value for player
    if illegal_move(direction, player.region):  # Check for illegal move
        draw.draw_text("There's nothing but open water that way, try somewhere else!")
        sound.play_sound("dialogue/nothing.wav")
        return_on_event("sound")
    else:
        if direction == 1:
            player.region -= 3  # North
        elif direction == 2:
            player.region -= 1  # West
        elif direction == 3:
            player.region += 3  # South
        elif direction == 4:
            player.region += 1  # East
        draw.draw_text("You start walking.")
        sound.play_sound("dialogue/walking.wav")


def illegal_move(direction, region):  # Check for illegal movement
    if region < 3 and direction == 1:  # Illegal move north
        return True
    if region % 3 == 0 and direction == 2:  # Illegal move west
        return True
    if region > 5 and direction == 3:  # Illegal move south
        return True
    if region > 5 and direction == 4:  # Illegal move east
        return True
    return False


def look(region, player):
    sounds = [""] * 3
    region = region[player.region]
    description = "You find yourself in a " + region.climate + ", "
    sounds[0] = "dialogue/yourself.wav"
    if region.climate == "cold":
        sounds[1] = "dialogue/cold.wav"
    elif region.climate == "fair":
        sounds[1] = "dialogue/fair.wav"
    elif region.climate == "warm":
        sounds[1] = "dialogue/warm.wav"

    if region.texture == "open":
        description += "open landscape. "
        sounds[2] = "dialogue/open.wav"
    elif region.texture == "forrest":
        description += 'green forrest. '
        sounds[2] = "dialogue/forrest.wav"
    elif region.texture == "mountains":
        description += "region of mountains."
        sounds[2] = "dialogue/mountain.wav"
    draw.draw_text(description)

    for i in sounds:
        if i != "":
            sound.play_sound(i)
            return_on_event("sound")

    if player.gold == 0 and region.item != 0:
        draw.draw_text("You also see something shimmering beneath some rocks."
                       "\nYou find a bag of gold!")
        sound.play_sound("dialogue/gold.wav")
        return_on_event("sound")
        player.gold = 1
    if player.region_shop_keeper == region.location:
        draw.draw_text("Hey, there is another person here!\n"
                       "He promises to get you home for a bag of gold.")
        sound.play_sound("dialogue/person.wav")
        return_on_event("sound")


def return_on_event(return_event, text=""):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            elif event.type == pg.KEYDOWN and return_event == "string":
                if event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                if event.key == pg.K_RETURN and text:
                    # draw.draw_text(text)  # Return checked last because
                    return text  # multiple presses can occur in one frame
        if not sound.is_playing() and return_event == "sound":
            return text

        draw.draw_input_box(text)
        draw.update()
        clock.tick(30)


def main():
    myplayer = Player()
    game_over = False

    draw.draw_background()
    draw.draw_text_box()
    draw.update()
    sound.play_soundtrack("soundtrack/")

    sound.play_sound("dialogue/welcome.wav")
    draw.draw_text("Welcome player!"
                   "\nYou find yourself stranded at an unknown location, feel free to explore!"
                   "\nPlease enter your name.")
    input_text = return_on_event("sound")
    myplayer.name = return_on_event("string", input_text)

    while not game_over:
        sound.play_sound("dialogue/action.wav")
        draw.draw_text("Choose an action: \n [1] Move north \n [2] Move west \n [3] Move south \n [4] Move east "
                       "\n [5] Look around")
        return_on_event("sound")
        try:
            action = int(float(return_on_event("string")))
        except:
            action = -1

        if not 0 < action < 6:
            draw.draw_text("Invalid input, please input a number from 1 to 5")
            sound.play_sound("dialogue/invalid.wav")
            return_on_event("sound")
        else:
            if action == 5:
                look(regions, myplayer)
                if myplayer.region == myplayer.region_shop_keeper and myplayer.gold:
                    draw.draw_text(
                        "You hand over the bag of gold and the magic shopkeeper throws powder in the air with "
                        "colorful sparks. "
                        "\nAnd you escape the island."
                        "\nCongratulations " + myplayer.name + "!")
                    sound.play_sound("dialogue/escape.wav")
                    return_on_event("sound")
                    draw.draw_text(" \n \nLead Programmer & Designer: Axel Söderberg\n"
                                   "Audio & Programming: Tintin Axelsson\n"
                                   "Voice Acting: Eric Ryberg")
                    game_over = True
            else:
                player_move(action, myplayer)
                return_on_event("sound")
    return_on_event("text")


if __name__ == '__main__':
    main()
