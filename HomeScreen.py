from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from functools import partial

class HomeScreen(MDScreen):
    pass

class FavouriteSpace(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(partial(self.check_if_empty), 1)

    def check_if_empty(self, *largs):
        if len(self.ids.space_for_cards.children) == 0:
            self.ids.space_for_cards.add_widget(MDLabel(
                id = "tempID",
                text = "You don't have any ToDo lists favourited, you can change this by pressing the star next to your ToDo lists!\n",
                size_hint = (1, .7),
                sapcing= "10dp",
                pos_hint = {"y": 0.1}
                
            ))
            self.height = self.calc_height()
        elif len(self.ids.space_for_cards.children) == 2:
            for child in self.ids.space_for_cards.children:
                if "MDLabel" in str(child) :
                    self.ids.space_for_cards.remove_widget(child)
                    self.height = self.calc_height()

    def calc_height(self):
        height = len(self.ids.space_for_cards.children) * 100
        return str(height + 60) + "dp"
        
                