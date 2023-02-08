from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime

'''Code For Calender Feature'''


'''Code for ToDo List pages'''

# ///Code for Creation and viewing of multiple ToDoLists///

# The Main screen for list creation  
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
        
        self.parent.add_widget(ToDoListPage(name=str(list_without_checkbox.text)))
        list_without_checkbox.bind(on_release= lambda x : self.change_screen(list_without_checkbox.text))
        self.ids["Container"].add_widget(list_without_checkbox)
        task.text = "" 
    
    # Allows for the changing of screens when a list item is pressed
    def change_screen(self, list_name):
        self.parent.get_screen(list_name).ids.ToDoListName.text = "[u][size=32][b]" + list_name + "[/b][/size][/u]"
        self.parent.current = list_name
        print(f"Changing screen to: {self.parent.current}")

# Each list item 
class ListItemWithoutCheckbox(OneLineAvatarIconListItem):
    # Allows for the deletion of items upon clicking the "bin" icon
    def delete_item(self, list_item):
        app = MDApp.get_running_app() # create instance of running app
        self.parent.remove_widget(list_item) # remove item from the list 
        print(f"Removing Screen: {list_item.text}")
        app.root.remove_widget(ToDoListPage(name=list_item.text)) # delete the screen

# The Dialog Box for creating a list 
class CreateListDialog(MDBoxLayout):
    pass

# ///Code For Individual ToDo List pages///

# ToDo list items 
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    # Allows users to complete tasks and see them crossed out 
    def mark(self, check, list_item):
        if check.active == True: # when a checkbox is ticked
            list_item.text = "[s]"+list_item.text+"[/s]" # add strike through format to completed tasks
        else:
            list_item.text = list_item.text.replace("[s]", "").replace("[/s]","") # remove strike through markup
    # Allows for the deletion of item upon clcking the "bin icon"
    def delete_item(self, list_item):
        self.parent.remove_widget(list_item)

# Checkbox for list items 
class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

# Dialog Box for creating list items 
class DialogContent(MDBoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str("") # set date text to todays date when user 
        # %A = Week Day, %d = Day, %B = Month name, %Y = Year
    # opens date picker instnace 
    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)

# Main screen for creating and managing list items 
class ToDoListPage(Screen):
    task_list_dialog = None
    # opens dialog box 
    def show_task_dialog(self):
        if not self.task_list_dialog: # if a dialog does not exits 
            self.task_list_dialog = MDDialog ( # define one 
                title="Create Task",
                type="custom",
                content_cls=DialogContent()
            )
        self.task_list_dialog.open() # open the dialog 
    # closes dialog box
    def close_dialog(self):
        self.task_list_dialog.dismiss()
    
    # Takes information from dialog box and creates a list item from it
    def add_task(self, task, task_date):
        print(f"Creating task: {task.text, task_date.text}")
        self.ids["Container"].add_widget(ListItemWithCheckbox(text="[b]"+task.text+"[/b]", secondary_text=task_date.text))
        task.text = ""
        task_date.text = ""

'''Main application'''
# loads styling and themes, creates and populates a screen manager
class MainApp(MDApp):
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.theme_style = "Dark"
        Builder.load_file("styling.kv")
        sm = ScreenManager()
        sm.add_widget(ToDoListView(name="ListView"))
        return sm

if __name__ == '__main__':
    app = MainApp()
    app.run()
