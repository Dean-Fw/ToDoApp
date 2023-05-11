from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch, OneLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.clock import Clock

from functools import partial

from JSON_Interface import JsonData


class ProjectCard(MDCard):
    pass

class LoadedProjectCard(ProjectCard):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loaded_content = content
        Clock.schedule_once(partial(self.apply_content))

    def apply_content(self, *largs):
        self.ids.project_title.text = self.loaded_content["project_name"] 

class ToDoListcard(MDCard):
    to_do_list_dialog = None
    options_menu = None
    def show_create_task_dialog(self):
        if not self.to_do_list_dialog:
            self.to_do_list_dialog = MDDialog( # define one 
                    title="Add a task",
                    type="custom",
                    content_cls=CreateTaskDialog(self),
                    auto_dismiss = False
                )
        self.to_do_list_dialog.open()

    def close_dialog(self):
        self.to_do_list_dialog.dismiss()
        self.to_do_list_dialog = None

    def open_drop_menu(self):
        app = MDApp.get_running_app()
        menu_items = [
            {
                "text": f"Delete List",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Delete List": self.delete_list(),
            },
            {
                "text": f"Edit List",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add List to a project": self.open_edit_list_dialog(),
            },
            {
                "text": f"Move List to a project",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add List to a project": self.open_move_list_dialog(),
            }
        ]
        if str(app.root.ids.screen_manager.current_screen) != "<Screen name='home'>":
            menu_items[2] = {
                "text": f"Move List to a folder",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add List to a folder": self.open_move_list_dialog(),
            }
            menu_items.append({
                "text": f"Move list to previous screen",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Add List to a project": self.move_list_to_previous_screen(),
            })

        self.options_menu = MDDropdownMenu(
            caller=self.ids.options_button,
            items=menu_items,
            width_mult=4,
        )
        self.options_menu.open()
    
    def delete_list(self):
        self.options_menu.dismiss()
        self.parent.remove_widget(self)
        JsonData("data.json").remove_list(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.ids.list_name_title.text)
    
    def open_edit_list_dialog(self):
        self.options_menu.dismiss()
        if not self.to_do_list_dialog:
            self.to_do_list_dialog = MDDialog( # define one 
                    title="Edit List",
                    type="custom",
                    content_cls=EditListDialog(self),
                    auto_dismiss = False
                )
        self.to_do_list_dialog.open()

    def open_move_list_dialog(self):
        self.options_menu.dismiss()
        if not self.to_do_list_dialog:
            self.to_do_list_dialog = MDDialog(
                title="Choose Project to move list to",
                type ="custom",
                content_cls=MoveListDialog(self),
                auto_dismiss = False
            )
        self.to_do_list_dialog.open()
    
    def move_list_to_previous_screen(self):
        JsonData("data.json").move_list(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.ids.list_name_title.text, MDApp.get_running_app().root.ids.screen_manager.current_screen.previous.name)

class CreateTaskDialog(MDBoxLayout):
    def __init__(self, card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_called_from = card
    
    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)

    def add_task(self):
        task_name = self.ids.task_text
        task_deadline = self.ids.date_text

        list_item = ListItemWithCheckbox(self.card_called_from, text=task_name.text, secondary_text=task_deadline.text)

        self.card_called_from.ids.to_do_list.add_widget(list_item)
        self.adjsut_list_height(self.card_called_from, list_item.height)
        task_json = {"task_name":task_name.text, "completed":False, "task_date": task_deadline.text}
        JsonData("data.json").append_new_task(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.card_called_from.ids.list_name_title.text, task_json)
        task_name.text = ""
        task_deadline.text = ""

    def adjsut_list_height(self, card, item_height):
        card.height = str(75 + (len(card.ids.to_do_list.children)*item_height)) + "dp"

    def close_dialog(self):
        self.card_called_from.close_dialog()

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, origin_card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_called_from = origin_card
    # Allows users to complete tasks and see them crossed out 
    def mark(self, check, list_item):
        if check.active == True: # when a checkbox is ticked
            list_item.text = "[s]"+list_item.text+"[/s]" # add strike through format to completed tasks
        else:
            list_item.text = list_item.text.replace("[s]", "").replace("[/s]","") # remove strike through markup
    # Allows for the deletion of item upon clcking the "bin icon"
        new_json_string = {"task_name": self.text.replace("[s]","").replace("[/s]",""), "completed": check.active, "task_date": self.secondary_text}
        print(list_item.text)
        JsonData("data.json").edit_task(MDApp.get_running_app().root.ids.screen_manager.current_screen.name,self.card_called_from.ids.list_name_title.text,self.text.replace("[s]","").replace("[/s]",""), new_json_string)
    
    def delete_item(self, list_item): 
        JsonData("data.json").remove_task(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, 
                             self.card_called_from.ids.list_name_title.text, 
                             self.text.replace("[s]","").replace("[/s]",""))
        
        self.parent.remove_widget(list_item)
        self.adjsut_list_height(list_item.height)
 

    
    def adjsut_list_height(self, item_height):
        card = self.card_called_from
        card.height = str(75 + (len(card.ids.to_do_list.children)*item_height)) + "dp"

    edit_task_dialog = None
    def open_edit_task_dialog(self):
        if not self.edit_task_dialog:
            self.edit_task_dialog = MDDialog(
                title="Edit a task",
                type="custom",
                content_cls=EditTaskDialog(self, self.card_called_from),
                auto_dismiss = False
            )
        self.edit_task_dialog.open()
    
    def close_edit_task_dialog(self):
        self.edit_task_dialog.dismiss()
        self.edit_task_dialog = None

# Checkbox for list items 
class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

class EditTaskDialog(MDBoxLayout):
    def __init__(self, list_item, card_called_from, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_to_edit = list_item
        self.ids.task_text.text = list_item.text
        self.ids.date_text.text = list_item.secondary_text
        self.card = card_called_from
    
    def edit_task(self):
        new_json_string = {"task_name": self.ids.task_text.text, "completed": self.item_to_edit.ids.check.active, "task_date":self.ids.date_text.text}
        JsonData("data.json").edit_task(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.card.ids.list_name_title.text, self.item_to_edit.text, new_json_string)
        self.item_to_edit.text = self.ids.task_text.text
        self.item_to_edit.secondary_text = self.ids.date_text.text
        
    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)

    def close_dialog(self):
        self.item_to_edit.close_edit_task_dialog()

class EditListDialog(MDBoxLayout):
    def __init__(self, card,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_to_edit = card
        self.ids.list_name_input.text = card.ids.list_name_title.text
    
    def edit_list(self):
        JsonData("data.json").edit_list(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.list_to_edit.ids.list_name_title.text, self.ids.list_name_input.text)
        self.list_to_edit.ids.list_name_title.text = self.ids.list_name_input.text
        

    def close_dialog(self):
        self.list_to_edit.close_dialog()

class MoveListDialog(MDBoxLayout):
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
        JsonData("data.json").move_list(MDApp.get_running_app().root.ids.screen_manager.current_screen.name, self.card_called_from.ids.list_name_title.text, self.project_screen.name)
        self.card_called_from.parent.remove_widget(self.card_called_from)
        self.project_screen.ids.Container.add_widget(self.card_called_from)
        self.card_called_from.close_dialog()

class LoadedToDoListCard(ToDoListcard):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loaded_content = content
        Clock.schedule_once(partial(self.apply_content))
    
    def apply_content(self, *largs):
        self.ids.list_name_title.text = self.loaded_content["list_name"]
        for i in self.loaded_content["list_items"]:
            loaded_task = ListItemWithCheckbox(self, text = i["task_name"], secondary_text= i["task_date"])
            if i["completed"] == True:
                loaded_task.ids.check.active = True
                loaded_task.mark(loaded_task.ids.check, loaded_task)
            self.ids.to_do_list.add_widget(loaded_task)
            loaded_task.adjsut_list_height(loaded_task.height)
    


