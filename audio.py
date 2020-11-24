import pygame as pg
import os
import threading
import time
import random


class SoundEngine:
    def __init__(self, directory="audio/"):
        pg.mixer.init()
        self.directory = directory
        self.queue = []
        self.thread = 0

    def __del__(self):
        self.x.join()
        pg.mixer.quit()

    def play_soundtrack(self, directory, theme="theme.wav"):
        directory = self.directory + directory
        list = os.listdir(directory)
        list.remove(theme)
        random.shuffle(list)
        pg.mixer.music.load(directory + theme)
        pg.mixer.music.play()

        def play_on_thread(songs):
            while True:
                for song in songs:
                    while pg.mixer.music.get_busy():
                        time.sleep(0.1)
                    pg.mixer.music.load(directory + song)
                    pg.mixer.music.play()

        self.x = threading.Thread(target=play_on_thread, args=(list,))
        self.x.start()

    def play_sound(self, file, block=False):
        sound = pg.mixer.Sound(self.directory + file)
        pg.mixer.Channel(0).play(sound)

        if block:
            while pg.mixer.Channel(0).get_busy():
                time.sleep(0.1)

    def is_playing(self):
        if pg.mixer.Channel(0).get_busy():
            return True
        else:
            return False

    def queue_sound(self, file):
        self.queue.append(self.directory + file)

    def play_queue(self):
        "Play Queue is currently always blocking"
        for current in self.queue:
            sound = pg.mixer.Sound(current)
            pg.mixer.Channel(0).play(sound)
            while pg.mixer.Channel(0).get_busy():
                time.sleep(0.1)
        self.queue = []
