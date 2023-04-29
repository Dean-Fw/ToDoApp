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

from ToDoCard import ProjectCard, ToDoListcard
from NoteCard import NoteCard

class HomeScreen(MDScreen):
        menu = None
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
                    "on_release": lambda x=f"Add image": self.test(),
                } 
            ]
            self.menu = MDDropdownMenu(
                caller=self.ids.plus_button,
                items=menu_items,
                width_mult=4,
            )
            self.menu.open()
        
        def test(self):
            print("test")
            self.menu.dismiss()
        
        dialog_box = None

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
            app.root.ids.screen_manager.add_widget(ProjectScreen(name = project_name))
            self.screen_called_from.ids.Container.add_widget(new_project_card)
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
    pass