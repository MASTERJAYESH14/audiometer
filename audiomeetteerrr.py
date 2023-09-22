from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import numpy as np
import sounddevice as sd

class SoundPlayer(BoxLayout):

    def play_sound(self, frequency, decibel_level):
        duration = 1.0  # Duration in seconds

        # Generate a 500 Hz sine wave
        t = np.linspace(0, duration, int(duration * 44100), False)
        wave = np.sin(2 * np.pi * frequency * t)

        # Scale the wave to the desired decibel level
        scaled_wave = np.power(10, decibel_level / 20) * wave

        # Play the sound
        sd.play(scaled_wave, samplerate=44100)

class SoundApp(App): 

    def build(self):
        return SoundPlayer()

if __name__ == '__main__':
    SoundApp().run()

