from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import Screen
from JSON_Interface import JsonData
from functools import partial
from kivy.clock import Clock

# class linked with list item rule 
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    # Allows users to complete tasks and see them crossed out 
    def mark(self, check, list_item):
        ScreenObject = self.parent.parent.parent.parent # This is almost the ugliest most stupidest most dumbest solution, but it's all i got :/
        if check.active == True: # when a checkbox is ticked
            list_item.text = "[s]"+list_item.text+"[/s]" # add strike through format to completed tasks
        else:
            list_item.text = list_item.text.replace("[s]", "").replace("[/s]","") # remove strike through markup
        
        json_data_obj = JsonData("data.json")
        json_data_obj.complete_task(list_item.text.replace("[b]", "").replace("[/b]", "").replace("[s]", "").replace("[/s]",""), ScreenObject.name.replace("[b]", "").replace("[/b]", ""))

    # Allows for the deletion of item upon clcking the "bin icon"
    def delete_item(self, list_item):
        ScreenObject = self.parent.parent.parent.parent # This is almost the ugliest most stupidest most dumbest solution, but it's all i got :/

        json_data_obj = JsonData("data.json")
        json_data_obj.remove_task(list_item.text.replace("[b]", "").replace("[/b]", ""), ScreenObject.name.replace("[b]", "").replace("[/b]", ""))

        print(f"Deleting item: {list_item.text}")
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
        json_data_obj = JsonData("data.json")
        print(f"Creating task: {task.text, task_date.text}")
        
        self.ids["Container"].add_widget(ListItemWithCheckbox(text="[b]"+task.text+"[/b]", secondary_text=task_date.text))
        parent_list = self.ids.ToDoListName.text.replace("[u]", "").replace("[/u]","").replace("[b]", "").replace("[/b]","")
        
        task_json = {"task_name":task.text, "completed":False, "task_date": task_date.text}
        json_data_obj.append_new_task(task_json, parent_list)
        
        task.text = ""
        task_date.text = ""

# child class of ToDoListPage for use when loading in pages from JSON file
class LoadedToDoListPage(ToDoListPage):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(partial(self.load_tasks))
    # load tasks from JSON file and place in list object
    def load_tasks(self, *largs):
        jsonDataObject = JsonData("data.json")
        parent_list_index = jsonDataObject.find_list(self.ids.ToDoListName.text.replace("[u]", "").replace("[/u]","").replace("[b]","").replace("[/b]", ""))
        print(f"Parent list index: {parent_list_index}")

        for i in jsonDataObject.data["lists"][parent_list_index]["tasks"]:
            loaded_task = ListItemWithCheckbox(text= "[b]" + i["task_name"] + "[/b]", secondary_text=i["task_date"])
            loaded_task.ids.check.active = i["completed"]
            if loaded_task.ids.check.active:
                loaded_task.text = "[s]" + loaded_task.text + "[/s]"
                self.ids["Container"].add_widget(loaded_task)