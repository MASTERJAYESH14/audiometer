import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
import pyaudio
import numpy as np

class SoundGeneratorApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create a graph to display audio data
        self.graph = Graph(xlabel='Frequency', ylabel='Decibels', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           xlog=False, ylog=False, x_grid=True, y_grid=True,
                           xmin=0, xmax=8000, ymin=-1, ymax=1)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.layout.add_widget(self.graph)

        # Create play and stop buttons
        self.play_button = Button(text="Play")
        self.play_button.bind(on_press=self.play_sound)
        self.stop_button = Button(text="Stop")
        self.stop_button.bind(on_press=self.stop_sound)

        # Add buttons to the layout
        self.layout.add_widget(self.play_button)
        self.layout.add_widget(self.stop_button)

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()

        return self.layout

    def play_sound(self, instance):
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        self.stream.start_stream()
        self.audio_playing = True

        self.frequencies = [250, 500, 1000, 2000, 4000, 8000]
        self.amplitude = 0.5
        self.duration = 1.0

        Clock.schedule_interval(self.generate_and_plot, 1.0/60.0)

    def generate_and_plot(self, dt):
        if not self.audio_playing:
            return

        t = np.linspace(0, self.duration, int(44100 * self.duration), endpoint=False)
        signal = np.zeros_like(t)

        for freq in self.frequencies:
            signal += self.amplitude * np.sin(2 * np.pi * freq * t)

        self.plot.points = [(i, val) for i, val in enumerate(signal)]

        self.stream.write(signal.tobytes())

    def stop_sound(self, instance):
        if self.audio_playing:
            self.audio_playing = False
            Clock.unschedule(self.generate_and_plot)
            self.stream.stop_stream()
            self.stream.close()

    def on_stop(self):
        self.p.terminate()

if __name__ == '__main__':
    SoundGeneratorApp().run()
