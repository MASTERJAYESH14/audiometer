import pyaudio
import numpy as np
import time
from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class SoundGeneratorApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        play_button = Button(text="Play Sounds")
        play_button.bind(on_press=self.play_sounds)
        layout.add_widget(play_button)
        return layout

    def play_sounds(self, instance):
        # Create a list of frequencies to play
        frequencies = [250, 500, 1000, 2000, 4000, 8000]

        # Create a list of desired dB levels
        db_levels = [-10, -5, 0, 5, 10, 15]

        # Create a PyAudio instance
        p = pyaudio.PyAudio()

        # Define the duration for each frequency (in seconds)
        duration = 2

        # Function to play sounds
        def play_sound(dt):
            for dB in db_levels:
                # Calculate the amplitude based on the dB level
                amplitude = 10 ** (dB / 20.0)

                for frequency in frequencies:
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

if __name__ == '__main__':
    SoundGeneratorApp().run()