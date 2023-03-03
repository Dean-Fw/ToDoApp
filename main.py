from kivymd.app import MDApp
from kivy.lang import Builder
<<<<<<< Updated upstream
from kivy.uix.screenmanager import ScreenManager
from ToDoListView import ToDoListView
=======
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty
from ToDoListView import ToDoListView
from HomeScreen import HomeScreen


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
>>>>>>> Stashed changes

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
