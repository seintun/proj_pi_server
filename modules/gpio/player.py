import pygame
import time
import os

class MP3Player:
    def __init__(self):
        """Initialize and play the given MP3 file until it ends."""
        self.running_server = '/home/ArthurPI5/Projects/GitHub/proj_pi_server/mp3/application_running_v3.mp3'
        self.hello = '/home/ArthurPI5/Projects/GitHub/proj_pi_server/mp3/hello_v3.mp3'

        # Configure SDL to use PulseAudio
        os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'

        try:
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
            print("Audio initialized with PulseAudio.")
            self.play_until_end(self.running_server)
        except pygame.error as e:
            print(f"Error initializing audio system: {e}")
            print("Available PulseAudio sinks:")
            os.system('pactl list short sinks')

    def play_until_end(self, file_path):
        """Plays an MP3 file until it finishes."""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            print(f'Playing: {file_path}')
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        except pygame.error as e:
            print(f"Error playing audio file {file_path}: {e}")

    def play_song_one(self):
        """Say Hello!"""
        self.play_until_end(self.hello)


mp3_player = MP3Player()