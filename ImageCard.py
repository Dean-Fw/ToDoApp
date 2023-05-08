from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class ImageCard(MDCard):
    def calculate_height(self):
        print(self.ids.image_space.norm_image_size) 
        #self.height = str(self.ids.image_space.norm_image_size + 20) + "dp"
