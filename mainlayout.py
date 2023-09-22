import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
Builder.load_file('whatever.kv')
class Mylayout(Widget):
    pass
    
class Myapp(App):
    def build(self):
        return Mylayout()
Myapp().run()
