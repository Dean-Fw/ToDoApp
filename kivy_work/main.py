from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("ToDo.kv")


MainApp().run()
