from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        Builder.load_file("ToDo.kv")
        return WindowManager()

MainApp().run()
