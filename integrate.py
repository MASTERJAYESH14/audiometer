from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

frequency=[250]
def play_sound(self, frequency, decibel_level):
        duration = 1.0  # Duration in seconds

        # Generate a 500 Hz sine wave
        t = np.linspace(0, duration, int(duration * 44100), False)
        wave = np.sin(2 * np.pi * frequency * t)

        # Scale the wave to the desired decibel level
        scaled_wave = np.power(10, decibel_level / 20) * wave

        # Play the sound
        sd.play(scaled_wave, samplerate=44100)
def decibel():
     decibel=0
def hear():
     decibel =decibel+5
    def barely():
     frequency=frequecy*2
plt.plot(x,y)
plt.ylabel("decibels")
plt.xlabel("Frequencies")

class graphs(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box=self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    def save_it(self):
        pass
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="BlueGray"
        Builder.load_file("graphing.kv")
        return graphs()
    
MainApp().run()