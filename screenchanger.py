from kivymd.app import MDApp #help in creating app
from kivymd.uix.button import MDFlatButton,MDFillRoundFlatIconButton,MDRectangleFlatButton
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.label import MDLabel, MDIcon
#from kivymd.uix.screen import Screen
from kivy.lang.builder import Builder
from kivy.uix.scatterlayout import ScatterLayout
from kivy.config import Config
from kivymd.uix.dialog import MDDialog

screen_helper="""
ScreenManager:
    Welcomescreen:
    Profilescreen:
    Dialogbox:

<Welcomescreen>:
    name: 'welcome'
    MDFillRoundFlatIconButton:
        text: 'Welcome to AudioMeter'
        pos_hint: {'center_x':0.5, 'center_y': 0.5}
        on_press: root.manager.current = 'profile'

<Profilescreen>:
    name: 'profile'
    MDTextField:
        hint_text: 'Enter Username'
        helper_text_mode: 'on_focus'
        icon_right: 'android'
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size_hint: (0.2,0.2)
        width: 300
    MDFlatButton:
        text: 'proceed'
        pos_hint: {'center_x':0.5, 'center_y':0.2}
        on_press: root.manager.current = 'box'
<Dialogbox>:
    name: 'box'
"""

class Welcomescreen(Screen):
    pass
class Profilescreen(Screen):
    pass
class Dialogbox(Screen):
    def build (self,obj):
        self.dialog=MDDialog(name='box',title='Disclaimer',text='hehe',size_hint=(0.7,1))
        self.dialog.open()
class Myscreenmanager(ScreenManager):
    pass


class AudioMeterApp(MDApp):
    def build(self):
        sm= Myscreenmanager()
        sm.add_widget(Welcomescreen(name='welcome'))
        sm.add_widget(Profilescreen(name='profile'))
        sm.add_widget(Dialogbox(name='box'))
        scr = Builder.load_string(screen_helper)
        return scr
AudioMeterApp().run()