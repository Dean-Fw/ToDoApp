from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.filemanager import MDFileManager

from functools import partial
import os

from JSON_Interface import JsonData

class ImageCard(MDCard):
    options_menu = None
    file_manager = None
    move_dialog = None
    def open_drop_menu(self):
        menu_items = [
            {
                "text": f"Delete Image",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Delete Image": self.delete_image(),
            },
            {
                "text": f"change Image",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"change Image": self.open_file_manager(),
            },
            {
                "text": f"Add Image to a project",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add Image to a project": self.open_move_image_dialog(),
            }
        ]
        self.options_menu = MDDropdownMenu(
            caller=self.ids.options_button,
            items=menu_items,
            width_mult=4,
        )
        self.options_menu.open()

    def delete_image(self):
        self.options_menu.dismiss()
        self.options_menu = None
        self.parent.remove_widget(self)
        JsonData("data.json").remove_image(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.ids.image_title.text)
        

    def open_move_image_dialog(self):
        self.options_menu.dismiss()
        if not self.move_dialog:
            self.move_dialog = MDDialog(
                title="Choose Project to move image to",
                type ="custom",
                content_cls=MoveImageDialog(self),
                auto_dismiss = False
            )
        self.move_dialog.open()

    def close_dialog(self):
        self.move_dialog.dismiss()
        self.move_dialog = None

    def open_file_manager(self):
        self.options_menu.dismiss()
        self.options_menu = None
        path = os.path.expanduser("~")
        self.file_manager = MDFileManager(
            exit_manager = self.close_manager,
            select_path = self.select_path,
            preview = True
        )
        self.file_manager.show(path)
    
    def close_manager(self, *args):
        self.file_manager.close()
        self.file_manager = None
    
    def select_path(self, path: str):
        if ".jpeg" or ".png" or ".jpeg" in path:
            self.ids.image_space.source = path
            self.ids.image_title.text = path
        self.close_manager()
    
class MoveImageDialog(MDBoxLayout):
    create_project_dialog = None
    def __init__(self, card,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_called_from = card
        self.populate_dialog()
        
    def populate_dialog(self):
        for child in self.ids.list_of_projects.children:
            if child.text != "Create new project":
                self.ids.list_of_projects.remove_widget(child)
        for child in self.card_called_from.parent.children:
            if "ProjectCard" in str(child):
                self.ids.list_of_projects.add_widget(ProjectListItem(self.card_called_from, child.ids.project_title.text, text = child.ids.project_title.text))

    def close_dialog(self):
        self.card_called_from.close_dialog()

    def create_new_project(self):
        app = MDApp.get_running_app()
        app.root.ids.screen_manager.current_screen.open_create_project_dialog()
        Clock.schedule_once(self.check_dialog_is_closed)
    
    def check_dialog_is_closed(self, dt):
        app = MDApp.get_running_app()
        if app.root.ids.screen_manager.current_screen.dialog_box == None:
            self.populate_dialog()
        else:
            Clock.schedule_once(self.check_dialog_is_closed, 0.1)

    
class ProjectListItem(OneLineListItem):
    create_move_project_dialog = None
    def __init__(self, card, project_page,*args, **kwargs):
        super().__init__(*args, **kwargs)
        app = MDApp.get_running_app()
        self.project_screen = app.root.ids.screen_manager.get_screen(project_page)
        self.card_called_from = card

    def move_list(self):
        self.card_called_from.parent.remove_widget(self.card_called_from)
        self.project_screen.ids.Container.add_widget(self.card_called_from)
        self.card_called_from.close_dialog()   

class LoadedImageCard(ImageCard):
    def __init__(self,content, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.loaded_content = content
        Clock.schedule_once(partial(self.apply_content))

    def apply_content(self, *largs):
        self.ids.image_space.source = self.loaded_content["source"]
        self.ids.image_title.text = self.loaded_content["name"] 
