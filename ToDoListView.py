from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from ToDoListPage import ToDoListPage
from JSON_Interface import JsonData
from kivy.clock import Clock
from functools import partial

class ToDoListView(Screen):
    def __init__(self, sm,**kw):
        super().__init__(**kw)
        Clock.schedule_once(partial(self.load_tasks, sm)) 
    ''' Methods for loading tasks from JSON file to screen'''
    def load_tasks(self, sm, *largs):
        json_data_object = JsonData("data.json")
        self.loaded_items = []

        for i in json_data_object.data["lists"]: 
            self.add_loaded_item_to_list(i)    

        for i in self.loaded_items:
            self.bind_on_release_to_loaded_item(sm, i) 

    def bind_on_release_to_loaded_item(self, sm, loaded_item):
        self.manager.add_widget(ToDoListPage(name = loaded_item.text))
        loaded_item.bind(on_release= lambda x: self.change_screen(loaded_item.text))
    
    def add_loaded_item_to_list(self, loaded_item):
            loaded_object = ListItemWithoutCheckbox(text="[b]" + loaded_item["list_name"] + "[/b]")
            self.ids["Container"].add_widget(loaded_object)
            self.loaded_items.append(loaded_object)

    task_list_dialog = None
    # Opens Dialog box that allows for the creation of classes 
    def show_task_dialog(self): 
        if not self.task_list_dialog: # if a dialog does not exits 
            self.task_list_dialog = MDDialog ( # define one 
                title="Create a ToDo list",
                type="custom",
                content_cls=CreateListDialog()
            )
        self.task_list_dialog.open() # open the dialog 

    # Closes dialog box 
    def close_dialog(self):
        self.task_list_dialog.dismiss()

    # Takes values returned from dialog box and adds it to the screen,
    # also creates a screen for the item and adds it to the screen manager
    def add_task(self, task):
        print(f"Creating list: {task.text}")
        list_without_checkbox = ListItemWithoutCheckbox(text="[b]" + task.text + "[/b]")
        
        json_data_obj = JsonData("data.json")
        json_data_obj.append_new_list({"list_name": task.text, "tasks": []})
        
        self.create_screen(list_without_checkbox)
       
        task.text = "" 
    
    # Allows for the changing of screens when a list item is pressed
    def change_screen(self, list_name):
        self.parent.get_screen(list_name).ids.ToDoListName.text = "[u][size=32][b]" + list_name + "[/b][/size][/u]"
        self.parent.current = list_name
        print(f"Changing screen to: {self.parent.current}")

    def create_screen(self, object):
        self.parent.add_widget(ToDoListPage(name=str(object.text)))
        object.bind(on_release= lambda x : self.change_screen(object.text))
        self.ids["Container"].add_widget(object)

class CreateListDialog(MDBoxLayout):
    pass

class ListItemWithoutCheckbox(OneLineAvatarIconListItem):
    # Allows for the deletion of items upon clicking the "bin" icon
    def delete_item(self, list_item):
        # Remove screen from app
        app = MDApp.get_running_app() # create instance of running app
        self.parent.remove_widget(list_item) # remove item from the list 
        print(f"Removing Screen: {list_item.text}")
        # Remove List from JSON file 
        json_data_obj = JsonData("data.json")
        json_data_obj.remove_list(list_item.text.replace("[b]", "").replace("[/b]",""))
        app.root.remove_widget(ToDoListPage(name=list_item.text)) # delete the screen
