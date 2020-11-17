import os, random, threading, time
import pygame


class SoundEngine:
    def __init__(self, directory="audio/"):
        pygame.mixer.init()
        self.directory = directory
        self.queue = []
        self.thread = 0

    def __del__(self):
        self.x.join()
        pygame.mixer.quit()

    def playSoundtrack(self, directory, theme="theme.wav"):
        list = os.listdir(directory)
        list.remove(theme)
        random.shuffle(list)
        pygame.mixer.music.load(directory+theme)
        pygame.mixer.music.play()

        def playOnThread(songs):
            while True:
                for song in songs:
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    pygame.mixer.music.load(directory+song)
                    pygame.mixer.music.play()
        self.x = threading.Thread(target=playOnThread, args=(list,))
        self.x.start()

    def playSound(self, file, block=True):
        sound = pygame.mixer.Sound(self.directory + file)
        pygame.mixer.Channel(0).play(sound)

        if block:
            while pygame.mixer.Channel(0).get_busy():
                time.sleep(0.1)

    def queueSound(self, file):
        self.queue.append(self.directory + file)

    def playQueue(self):
        "Play Queue is currently always blocking"
        for current in self.queue:
            sound = pygame.mixer.Sound(current)
            pygame.mixer.Channel(0).play(sound)
            while pygame.mixer.Channel(0).get_busy():
                time.sleep(0.1)
        self.queue = []

