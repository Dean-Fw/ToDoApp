from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.list import OneLineListItem
from functools import partial

class NoteCard(MDCard):
    options_menu = None
    note_dialog = None
    def open_drop_menu(self):
        menu_items = [
            {
                "text": f"Delete Note",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Delete Note": self.delete_note(),
            },
            {
                "text": f"Edit Note",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Edit Note": self.open_edit_note_dialog(),
            },
            {
                "text": f"Add Note to a project",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add List to a project": self.open_move_note_dialog(),
            }
        ]
        self.options_menu = MDDropdownMenu(
            caller=self.ids.options_button,
            items=menu_items,
            width_mult=4,
        )
        self.options_menu.open()
    
    def delete_note(self):
        self.options_menu.dismiss()
        self.options_menu = None
        self.parent.remove_widget(self)

    def calculate_height(self):
        self.height = str(self.ids.note_title.height + self.ids.note.height+ 20) + "dp"

    def open_edit_note_dialog(self):
        if self.options_menu:
            self.options_menu.dismiss()
            self.options_menu = None
        if not self.note_dialog:
            self.note_dialog = MDDialog( # define one 
                    title="Edit Note",
                    type="custom",
                    content_cls=EditNoteDialog(self),
                    auto_dismiss = False
                )
        self.note_dialog.open()

    def open_move_note_dialog(self):
        self.options_menu.dismiss()
        if not self.note_dialog:
            self.note_dialog = MDDialog(
                title="Choose Project to move note to",
                type ="custom",
                content_cls=MoveNoteDialog(self),
                auto_dismiss = False
            )
        self.note_dialog.open()
    
    def close_dialog(self):
        self.note_dialog.dismiss()
        self.note_dialog = None

    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.deadline.text = str(date)

class EditNoteDialog(MDBoxLayout):
    def __init__(self, card,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.note_to_edit = card
        self.ids.note_title_text.text = card.ids.note_title.text
        self.ids.note.text = card.ids.note.text
    
    def edit_note(self):
        self.note_to_edit.ids.note_title.text = self.ids.note_title_text.text
        self.note_to_edit.ids.note.text = self.ids.note.text
        self.note_to_edit.ids.deadline.text = self.ids.date_text.text
        self.note_to_edit.calculate_height()
    
    def close_dialog(self):
        self.note_to_edit.close_dialog()

    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)

class MoveNoteDialog(MDBoxLayout):
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

class LoadedNoteCard(NoteCard):
    def __init__(self, content,*args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(partial(self.apply_content))
        self.loaded_content = content
        
    def apply_content (self, *largs):
        self.ids.note_title.text = self.loaded_content["note_title"]
        self.ids.note.text = self.loaded_content["note"]
        self.ids.deadline.text = self.loaded_content["deadline"]
        self.calculate_height()
