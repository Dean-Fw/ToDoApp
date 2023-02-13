from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from ToDoListPage import ToDoListPage
from jsonExperiment import JsonData




class ToDoListView(Screen):
    task_list_dialog = None
    # Opens Dialog box that allows for the crration of classes 
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
        self.parent.add_widget(ToDoListPage(name=str(list_without_checkbox.text)))
        list_without_checkbox.bind(on_release= lambda x : self.change_screen(list_without_checkbox.text))
        self.ids["Container"].add_widget(list_without_checkbox)
        task.text = "" 
    
    # Allows for the changing of screens when a list item is pressed
    def change_screen(self, list_name):
        self.parent.get_screen(list_name).ids.ToDoListName.text = "[u][size=32][b]" + list_name + "[/b][/size][/u]"
        self.parent.current = list_name
        print(f"Changing screen to: {self.parent.current}")

class CreateListDialog(MDBoxLayout):
    pass

class ListItemWithoutCheckbox(OneLineAvatarIconListItem):
    # Allows for the deletion of items upon clicking the "bin" icon
    def delete_item(self, list_item):
        app = MDApp.get_running_app() # create instance of running app
        self.parent.remove_widget(list_item) # remove item from the list 
        print(f"Removing Screen: {list_item.text}")
        json_data_obj = JsonData("data.json")
        json_data_obj.remove_list(list_item.text.replace("[b]", "").replace("[/b]",""))
        app.root.remove_widget(ToDoListPage(name=list_item.text)) # delete the screen
