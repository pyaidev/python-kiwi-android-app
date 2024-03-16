from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from googletrans import Translator
from gtts import gTTS
import pygame

KV = '''
ScreenManager:
    MenuScreen:
    DictionaryScreen:
    TranslatorScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDLabel:
            text: 'Выберите действие:'

        # image: 'logo.png'
        Image:
            source: 'img.png'
            size_hint: 3, 3
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            allow_stretch: True


        MDRaisedButton:
            text: 'Словарь'
            on_release: root.manager.current = 'dictionary'
            on_release: app.dictionary()
            spacing: dp(10)
            padding: dp(10)
            halign: 'center'




        MDRaisedButton:
            text: 'Переводчик'
            on_release: root.manager.current = 'translator'


<DictionaryScreen>:
    name: 'dictionary'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDLabel:
            text: 'Словарь:'
            halign: 'center'
            theme_text_color: 'Primary'
            font_style: 'H6'




        MDLabel:
            id: word_list
            text: ''
            halign: 'center'
            theme_text_color: 'Primary'
            font_style: 'H6'

        MDRaisedButton:
            text: 'Назад'
            on_release: root.manager.current = 'menu'


        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)

            MDRaisedButton:
                id: prev_page_button
                text: "<< Предыдущая страница"
                on_release: app.dictionary(page=max(1, app.page - 1))

            MDRaisedButton:
                id: next_page_button
                text: 'Следующая страница >>'
                on_release: app.dictionary(page=app.page + 1)










<TranslatorScreen>:
    name: 'translator'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDLabel:
            text: 'Введите слово на узбекском:'

        MDTextField:
            id: input_text
            multiline: False

        MDLabel:
            text: 'Перевод на английском:'

        MDTextField:
            id: output_text
            multiline: False
            readonly: True

        MDRaisedButton:
            text: 'Перевести'
            on_release: app.translate_text()
            # on_release: root.manager.current = 'menu'

        MDRaisedButton:
            text: 'Назад'
            on_release: root.manager.current = 'menu'
'''

class MenuScreen(Screen):
    pass

class DictionaryScreen(Screen):
    pass

class TranslatorScreen(Screen):
    pass

class DictionaryApp(MDApp):

    def build(self):
        with open("uzb-eng.txt", "r", encoding="utf-8") as file:
            text = file.read()
            words = text.split("\n")
            self.words_en_uz = {}
            for word in words:
                if word:
                    if " - " in word:
                        en, uz = word.split(" - ", 1)
                        self.words_en_uz[en.strip()] = uz.strip()

                    else:
                        print(f"Ignoring invalid line: {word}")

        self.page = 1
        pygame.init()
        return Builder.load_string(KV)

    def search_dictionary(self):
        search_query = self.root.get_screen('dictionary').ids.search_input.text.lower()
        filtered_words = {key: value for key, value in self.words_en_uz.items() if search_query in key.lower() or search_query in value.lower()}

        word_list = ""
        for word, translation in filtered_words.items():
            word_list += f"{word} ----- {translation}\n"
        self.root.get_screen('dictionary').ids.word_list.text = word_list

    def translate_text(self):
        input_text = self.root.get_screen('translator').ids.input_text.text
        translator = Translator()
        translation = translator.translate(input_text, dest='en')
        translated_text = translation.text
        self.root.get_screen('translator').ids.output_text.text = translation.text
        self.speak_text(translated_text)

    def speak_text(self, text):
        language = 'en'  # Assuming the translated text is in English
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save("translated_text.mp3")
        pygame.mixer.music.load("translated_text.mp3")
        pygame.mixer.music.play()

    def on_start(self):
        toast("Добро пожаловать в словарь и переводчик!")

    def dictionary(self, page=None, words_per_page=10):
        if page is not None:
            self.page = page
        start_index = (self.page - 1) * words_per_page
        end_index = self.page * words_per_page
        current_page_words = list(self.words_en_uz.keys())[start_index:end_index]
        word_list = ""
        for word in current_page_words:
            word_list += f"{word} - {self.words_en_uz[word]}\n"
        self.root.get_screen('dictionary').ids.word_list.text = word_list
        has_next_page = end_index < len(self.words_en_uz)
        self.root.get_screen('dictionary').ids.next_page_button.disabled = not has_next_page

        self.root.get_screen('dictionary').ids.prev_page_button.disabled = self.page <= 1


if __name__ == '__main__':
    DictionaryApp().run()






