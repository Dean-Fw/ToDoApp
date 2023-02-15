from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import Screen
from JSON_Interface import JsonData

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
        json_data_obj = JsonData("data.json")
        json_data_obj.remove_task()

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
        json_data_obj = JsonData("data.json")
        print(f"Creating task: {task.text, task_date.text}")
        self.ids["Container"].add_widget(ListItemWithCheckbox(text="[b]"+task.text+"[/b]", secondary_text=task_date.text))
        parent_list = self.ids.ToDoListName.text.replace("[u]", "").replace("[/u]","").replace("[size=32]", "").replace("[/size]","").replace("[b]", "").replace("[/b]","")
        print(parent_list)
        task_json = {"task_name":task.text, "completed":False, "task_date": task_date.text}
        json_data_obj.append_new_task(task_json, parent_list)
        task.text = ""
        task_date.text = ""