import kivy
import numpy as np
import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.clock import Clock

kivy.require('1.11.1')

class HearingTestApp(App):
    def build(self):
        self.title = "Audiometer App"
        self.layout = BoxLayout(orientation='vertical', spacing=10)
        self.username_input = TextInput(hint_text="Enter Username")
        self.layout.add_widget(self.username_input)
        self.login_button = Button(text="Login", on_press=self.login)
        self.layout.add_widget(self.login_button)
        self.user_label = Label(text="")
        self.layout.add_widget(self.user_label)
        self.instructions_label = Label(
            text="Press 'Play' to hear a sound and indicate if you can hear it.")
        self.play_button = Button(
            text="Play", on_press=self.play_sound)
        self.layout.add_widget(self.instructions_label)
        self.layout.add_widget(self.play_button)
        self.sound = None
        self.user_responses = []
        self.frequency_slider = Slider(
            min=100, max=10000, value=1000, step=10)
        self.layout.add_widget(self.frequency_slider)
        self.results_button = Button(
            text="View Results", on_press=self.show_results)
        self.layout.add_widget(self.results_button)
        self.session = 1

        return self.layout

    def login(self, instance):
        username = self.username_input.text.strip()
        if username:
            self.user_label.text = f"User: {username}"
        else:
            self.user_label.text = "Please enter a valid username."

    def play_sound(self, instance):
        if self.sound:
            self.sound.stop()
        frequency = self.frequency_slider.value
        duration = 1.0
        t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
        audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
        self.sound = SoundLoader.load('sound.wav')  # Replace with your audio file path
        self.sound.seek(0)
        self.sound.queue(audio_data.tobytes())
        self.sound.play()
        Clock.schedule_once(self.ask_user_response, duration)

    def ask_user_response(self, dt):
        response = input("Did you hear the sound? (yes/no): ").strip().lower()
        self.user_responses.append({
            'session': self.session,
            'frequency': self.frequency_slider.value,
            'response': response,
        })
        self.frequency_slider.value = np.random.uniform(100, 10000)

    def show_results(self, instance):
        if self.user_responses:
            results_text = "Hearing Test Results:\n\n"
            for response in self.user_responses:
                results_text += f"Session: {response['session']} - Frequency: {response['frequency']} Hz - Response: {response['response']}\n"

            self.popup = ResultsPopup(title='Results', results_text=results_text)
            self.popup.open()
        else:
            self.popup = NoResultsPopup(title='No Results', no_results_text='No results to display.')
            self.popup.open()

    def on_stop(self):
        self.save_results()

    def save_results(self):
        with open('hearing_test_results.csv', 'a', newline='') as csvfile:
            fieldnames = ['session', 'frequency', 'response']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerows(self.user_responses)

        self.session += 1


class ResultsPopup(Popup):
    def __init__(self, results_text, **kwargs):
        super(ResultsPopup, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False

        content = BoxLayout(orientation='vertical', spacing=10)
        self.results_label = Label(text=results_text, size_hint=(1, 0.9))
        content.add_widget(self.results_label)
        close_button = Button(text='Close', size_hint=(1, 0.1))
        close_button.bind(on_release=self.dismiss)
        content.add_widget(close_button)
        self.add_widget(content)


class NoResultsPopup(Popup):
    def __init__(self, no_results_text, **kwargs):
        super(NoResultsPopup, self).__init__(**kwargs)
        self.size_hint = (0.6, 0.6)
        self.auto_dismiss = False

        content = BoxLayout(orientation='vertical', spacing=10)
        self.no_results_label = Label(
            text=no_results_text, size_hint=(1, 0.8))
        content.add_widget(self.no_results_label)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        close_button.bind(on_release=self.dismiss)
        content.add_widget(close_button)
        self.add_widget(content)


if __name__ == '__main__':
    HearingTestApp().run()

