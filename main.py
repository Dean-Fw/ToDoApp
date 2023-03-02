from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from ToDoListView import ToDoListView
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

# loads styling and themes, creates and populates a screen manager
class MainApp(MDApp):
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.theme_style = "Dark"
        kv = Builder.load_file("styling.kv")
        return kv

if __name__ == '__main__':
    app = MainApp()
    app.run()
