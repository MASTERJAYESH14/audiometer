from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
# Define what we want to graph X = []]
x = [0, 250, 500, 1000, 2000, 4000, 8000]
y = [0, 5, 10, 15, 20, 25, 30]

plt.plot(x,y)
plt.ylabel("Frequencies")
plt.xlabel("Decibals")

class plotting(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = self.ids.box
        box.add_widgets(FigureCanvasKivyAgg(plt.gcf()))

    def save_it(self):
        pass
class MainApp (MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file('graphsss.kv')
        return plotting()
    

MainApp().run()