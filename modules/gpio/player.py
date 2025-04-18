import pygame
import time

class MP3Player:
    def __init__(self):
        """Initialize and play the given MP3 file until it ends."""
        self.running_server = 'mp3/application_running_v2.mp3'
        self.hello = 'mp3/hello_v2.mp3'

        pygame.mixer.init()
        self.play_until_end(self.running_server)

    def play_until_end(self, file_path):
        """Plays an MP3 file until it finishes."""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f'Playing: {file_path}')
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def play_song_one(self):
        """Say Hello!"""
        self.play_until_end(self.hello)


mp3_player = MP3Player()