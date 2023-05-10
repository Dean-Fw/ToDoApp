from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock

import os
from functools import partial

from ToDoCard import ProjectCard, LoadedProjectCard, ToDoListcard, LoadedToDoListCard
from NoteCard import NoteCard, LoadedNoteCard
from ImageCard import ImageCard, LoadedImageCard
from JSON_Interface import JsonData


class HomeScreen(MDScreen):
    menu = None
    dialog_box = None
    file_manager = None
    json_file = JsonData("data.json").data
    screen_data = json_file["screens"][0]["cards"]
    screen_index = 0
    
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(partial(self.load_items, self.screen_data))
    
    def load_items(self, screen_cards,*largs):
        for i in screen_cards:
            if i["type"] == "note":
                card_to_load = LoadedNoteCard(i["content"])
                self.ids.Container.add_widget(card_to_load)
            elif i["type"] == "image":
                card_to_load = LoadedImageCard(i["content"])
                self.ids.Container.add_widget(card_to_load)
            elif i["type"] == "list":
                card_to_load = LoadedToDoListCard(i["content"])
                self.ids.Container.add_widget(card_to_load)
            elif i["type"] == "project":
                card_to_load = LoadedProjectCard(i["content"])
                app = MDApp.get_running_app()
                screen_to_load = LoadedProjectScreen(i["content"]["project_name"], app.root.ids.screen_manager.current_screen)
                
                app.root.ids.screen_manager.add_widget(screen_to_load)
                app.root.ids.nav_menu.add_widget(UserCreatedProjectListItem(text = i["content"]["project_name"]))
                self.ids.Container.add_widget(card_to_load)


            

    # method that opens a menu allowing the user to create an object of choice 
    def open_dropdown_menu(self):
        menu_items = [
            {
                "text": f"Add a Project",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add a Project": self.open_create_project_dialog(),
            },
            {
                "text": f"Add a To do list",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add a To do list": self.open_create_list_dialog(),
            },
            {
                "text": f"Add a Note",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add a Note": self.open_create_note_dialog(),
            },  
            {
                "text": f"Add image",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add image": self.open_file_manager(),
            } 
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.plus_button,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()
    
    def open_file_manager(self):
        self.menu.dismiss()
        self.menu = None
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
            new_card = ImageCard()
            new_card.ids.image_space.source = path
            new_card.ids.image_title.text = path
            self.ids.Container.add_widget(new_card)
            
            # append JSON file
            json_obj = JsonData("data.json")
            json_string = {"type":"image", "content":{"source":path,"name":path}}
            json_obj.append_new_card(self.screen_index,json_string)
        
        self.close_manager()
    # opens a dialog box to allow a user to 
    def open_create_project_dialog(self):
        if self.menu:
            self.menu.dismiss()      
         # Opens Dialog box that allows for the creation of classes
        if not self.dialog_box: # if a dialog does not exits 
            self.dialog_box = MDDialog( # define one 
                title="Create a Project",
                type="custom",
                content_cls=CreateProjectDialog(self),
                auto_dismiss = False
            )
        self.dialog_box.open() # open the dialog 
    
    def open_create_list_dialog(self):
        self.menu.dismiss()
         # Opens Dialog box that allows for the creation of classes
        if not self.dialog_box: # if a dialog does not exits 
            self.dialog_box = MDDialog( # define one 
                title="Create a to do list",
                type="custom",
                content_cls=CreateListDialog(self),
                auto_dismiss = False
            )
        self.dialog_box.open() # open the dialog 
    def open_create_note_dialog(self):
        self.menu.dismiss()
         # Opens Dialog box that allows for the creation of classes
        if not self.dialog_box: # if a dialog does not exits 
            self.dialog_box = MDDialog( # define one 
                title="Create a Note!",
                type="custom",
                content_cls=CreateNoteDialog(self),
                auto_dismiss = False
            )
        self.dialog_box.open() # open the dialog 
# Closes dialog box 
    def close_dialog(self):
        self.dialog_box.dismiss()
        self.dialog_box = None

class UserCreatedProjectListItem(MDNavigationDrawerItem):
    pass

class CreateProjectDialog(MDBoxLayout):
    def __init__(self, screen,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_called_from = screen
    # Variable to hold error dialog
    error_dialog = None
    # method that adds a created project card to the home screen and a short cut to the nav bar
    def create_project(self):
        project_name = self.ids.project_name_input.text

        new_project_card = ProjectCard()
        new_project_card.ids.project_title.text = project_name

        app = MDApp.get_running_app()
        
        # check whether a screen already exists with the same name and show an error dialog if so
        if project_name not in app.root.ids.screen_manager.screen_names:
            app.root.ids.screen_manager.add_widget(ProjectScreen(app.root.ids.screen_manager.current_screen, len(JsonData("data.json").data["screens"]),name = project_name))
            self.screen_called_from.ids.Container.add_widget(new_project_card)
            
            json_string_card = {"type":"project", "content":{"project_name":project_name}}
            json_string_screen = {"name":project_name, "previous":app.root.ids.screen_manager.current_screen.name,"cards":[]}
            JsonData("data.json").append_new_card(self.screen_called_from.screen_index, json_string_card)
            JsonData("data.json").append_new_screen(json_string_screen)

            if app.root.ids.topBar.title == "Home":
                app.root.ids.nav_menu.add_widget(UserCreatedProjectListItem(text = project_name))
        else:
            self.show_error_dialog("Error: You already have a project called \"" + project_name + "\"")
        
        self.ids.project_name_input.text = ""

    def show_error_dialog(self, error_text):
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                text= error_text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.dismiss_error_dialog
                    ),
                ],
                auto_dismiss = False
            )
        self.error_dialog.open()
    
    def dismiss_error_dialog(self, inst):
        self.error_dialog.dismiss()

    def dismiss_self(self):
        self.screen_called_from.close_dialog()
    
class CreateListDialog(MDBoxLayout):
    def __init__(self, screen,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_called_from = screen
    # Variable to hold error dialog
    error_dialog = None
    task_create_dialog = None
    # method that adds a created project card to the home screen and a short cut to the nav bar
    def create_to_do_list(self):
        list_name = self.ids.list_name_input.text

        new_list_card = ToDoListcard(id=list_name)
        new_list_card.ids.list_name_title.text = list_name

        # check whether a screen already exists with the same name and show an error dialog if so
        if len(list_name) > 0:
            self.screen_called_from.ids.Container.add_widget(new_list_card)

            # append JSON file
            json_string = {"type":"list", "content":{"list_name":list_name,"list_items":[]}}
            JsonData("data.json").append_new_card(self.screen_called_from.screen_index, json_string)
        else:
            self.show_error_dialog("Error: Your To do list has no name!")
        
        self.ids.list_name_input.text = ""

    def show_error_dialog(self, error_text):
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                text= error_text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.dismiss_error_dialog
                    ),
                ],
                auto_dismiss = False
            )
        self.error_dialog.open()

    def dismiss_error_dialog(self, inst):
        self.error_dialog.dismiss()
    
    def dismiss_self(self):
        self.screen_called_from.close_dialog()     


class CreateNoteDialog(MDBoxLayout):
    
    def __init__(self, screen,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin_screen = screen
    # Variable to hold error dialog
    error_dialog = None
    task_create_dialog = None
    # method that adds a created project card to the home screen and a short cut to the nav bar
    def create_note(self):
        note_name = self.ids.note_title_text.text

        new_note_card = NoteCard(id=note_name)
        new_note_card.ids.note_title.text = note_name
        new_note_card.ids.note.text = self.ids.note.text
        new_note_card.ids.deadline.text = self.ids.date_text.text
        new_note_card.calculate_height()
        
        # check whether a screen already exists with the same name and show an error dialog if so
        if len(self.ids.note.text) > 0:
            self.origin_screen.ids.Container.add_widget(new_note_card)

            # append to json
            json_string = {"type":"note", "content":{"note_title":note_name, "note":self.ids.note.text, "deadline":self.ids.date_text.text}}
            JsonData("data.json").append_new_card(self.origin_screen.screen_index, json_string)
        else:
            self.show_error_dialog("Error: Your note is empty!")
        
        self.ids.note_title_text = ""
        self.ids.note.text = ""

    def show_error_dialog(self, error_text):
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                text= error_text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.dismiss_error_dialog
                    ),
                ],
                auto_dismiss = False
            )
        self.error_dialog.open()

    def close_dialog(self):
        self.origin_screen.close_dialog()

    def dismiss_error_dialog(self, inst):
        self.error_dialog.dismiss()

    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)

class ProjectScreen(HomeScreen):
    def __init__(self, previous_screen, index,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous = previous_screen
        self.screen_index = index
    
    def load_items(self, screen_cards, *largs): # This is bad but it works ...
        pass

class LoadedProjectScreen(HomeScreen):
    def __init__(self, screen_name, previous_screen, *args, **kwargs):
        self.name = screen_name
        self.previous = previous_screen
        self.screen_data, self.screen_index = self.find_content()
        super().__init__(*args, **kwargs)
                
    def find_content(self):
        for i in self.json_file["screens"]:
            if i["name"] == self.name:
                return i["cards"], self.json_file["screens"].index(i)