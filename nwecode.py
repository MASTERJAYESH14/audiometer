import pyaudio
import numpy as np
import time
import kivy
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class SoundGeneratorApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        play_button = MDFlatButton(text="Play Sounds")
        play_button.bind(on_press=self.play_sounds)
        layout.add_widget(play_button)
        return layout

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stream = None  # Initialize stream as an instance variable

    def play_sounds(self, instance):
        # Create a list of frequencies to play
        frequencies = [250, 500, 1000, 2000, 4000, 8000]

        # Create a list of desired dB levels
        db_levels = [-10, -5, 0, 5, 10, 15]

        # Create a PyAudio instance
        p = pyaudio.PyAudio()

        # Define the duration for each frequency (in seconds)
        duration = 2

        # Get the index of the desired output device
        desired_device_name = "Speaker(Realtek(R) Audio)"
        output_device_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info["name"] == desired_device_name:
                output_device_index = i
                break

        # Open the audio stream
        if output_device_index is not None:
            try:
                self.stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True,
                    output_device_index=output_device_index
                )
                self.stream.start_stream()
            except Exception as e:
                print(f"Error opening audio stream: {e}")

        # Function to play sounds
        def play_sound(dt):
            for dB in db_levels:
                # Calculate the amplitude based on the dB level
                amplitude = 10 ** (dB / 20.0)

                for frequency in frequencies:
                    # Generate the sine wave for the current frequency with the specified amplitude
                    t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
                    signal = amplitude * np.sin(2 * np.pi * frequency * t)

                    # Write the signal to the stream and wait for the duration
                    self.stream.write(signal.tobytes())
                    time.sleep(duration)

            # Stop and close the stream
            self.stream.stop_stream()
            self.stream.close()

            # Terminate the PyAudio instance
            p.terminate()

        # Schedule sound generation for the next frame
        Clock.schedule_once(play_sound, 0)

if __name__ == '__main__':
    SoundGeneratorApp().run()
