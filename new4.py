import pyaudio
import numpy as np
import time
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('startfile.kv')

class Mylayout(Widget):

    frequencies = [250, 500, 1000, 2000, 4000, 8000]
    decibel_levels = [0]
    barely_audible_decibel_levels = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def play_sounds(self, frequencies, decibel_levels):
        p = pyaudio.PyAudio()

        # Define the duration for each frequency (in seconds)
        duration = 10

        # Function to play sounds
        def play_sound(dt):
            for frequency, decibel_level in zip(frequencies, decibel_levels):
                # Calculate the amplitude based on the dB level
                amplitude = 10 ** (decibel_level / 20.0)

                # Generate the sine wave for the current frequency with the specified amplitude
                t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
                signal = amplitude * np.sin(2 * np.pi * frequency * t)

                # Open an audio output stream
                stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
                stream.start_stream()

                # Write the signal to the stream and wait for the duration
                stream.write(signal.tobytes())
                time.sleep(duration)

                # Stop and close the stream
                stream.stop_stream()
                stream.close()

        Clock.schedule_once(play_sound, 0)  # Schedule sound generation for the next frame

        # Terminate the PyAudio instance
        p.terminate()

    def can_hear(self, frequencies, decibel_levels):
        for i in range(len(decibel_levels)):
            decibel_levels[i] -= 5
        self.play_sounds(frequencies, decibel_levels)

    def cannot_hear(self, frequencies, decibel_levels):
        for i in range(len(decibel_levels)):
            decibel_levels[i] += 5
        self.play_sounds(frequencies, decibel_levels)

    def barely_audible(self, decibel_levels, frequencies):
        for i in range(len(decibel_levels)):
            self.barely_audible_decibel_levels.append(decibel_levels[i])
        self.play_sounds(frequencies, decibel_levels)

class DesibelsApp(App):
    def build(self):
        self.p = pyaudio.PyAudio()
        return Mylayout()

DesibelsApp().run()