from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from ToDoListView import ToDoListView

# loads styling and themes, creates and populates a screen manager
class MainApp(MDApp):
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.theme_style = "Dark"
        Builder.load_file("styling.kv")
        sm = ScreenManager()
        sm.add_widget(ToDoListView(sm,name = "ListView"))
        return sm

if __name__ == '__main__':
    app = MainApp()
    app.run()
