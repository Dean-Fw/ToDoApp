from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class ImageCard(MDCard):
    def calculate_height(self):
        print(self.ids.image_space.height) 
        self.height = str(self.ids.image_space.height + 20) + "dp"
