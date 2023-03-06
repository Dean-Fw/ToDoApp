from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    pass

class FavouriteSpace(MDBoxLayout):
    def calc_height(self):
        height = len(self.ids.space_for_cards.children) * 100
        return str(height + 60) + "dp"
        
                