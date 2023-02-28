from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp
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

class SaveEditedTaskButton(MDRaisedButton):
    pass
class SaveNewTaskButton(MDRaisedButton):
    pass

# Abstract calss for Dialog Box for creating task items 
class DialogContent(MDBoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str("")

    #opens date picker dialog 
    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    # saves date when selected 
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)

# Child of DialogContent created to allow for editing of tasks
class EditTaskDialogContent(DialogContent):
    def __init__(self,object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_item = object
        Clock.schedule_once(partial(self.get_task_details,self.parent_item.text, self.parent_item.secondary_text))
        #self.ids.save_button.bind(on_release = lambda x : self.edit_task(task_name,task_date, self.parent_item))
   
    def get_task_details(self,task_name, task_date, *largs):
        self.ids.task_text.text =  task_name.replace("[b]", "").replace("[/b]", "")
        self.ids.date_text.text = task_date
        self.ids.save_or_exit.add_widget(SaveEditedTaskButton())
         
    def edit_task(self):
        print(self.ids.task_text.text)
        self.edit_JSON([self.ids.task_text.text, self.ids.date_text.text])
        self.parent_item.text = "[b]" + self.ids.task_text.text + "[/b]"
        self.parent_item.secondary_text = self.ids.date_text.text

    def edit_JSON(self, new_task_data):
        app = MDApp.get_running_app()
        json_data_obj = JsonData("data.json")
        
        parent_list_name = app.root.current_screen.ids.ToDoListName.text.replace("[u]", "").replace("[/u]","").replace("[b]", "").replace("[/b]","")
        task_name = self.parent_item.text.replace("[b]", "").replace("[/b]", "")

        json_data_obj.edit_task(new_task_data, task_name, parent_list_name)


        

# child of dialog content to allow for creation of tasks 
class CreateTaskDialogContent(DialogContent):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str("")
        self.ids.save_or_exit.add_widget(SaveNewTaskButton())
    
    def add_task(self):
        task_name = self.ids.task_text
        task_deadline = self.ids.date_text
        
        app = MDApp.get_running_app()
        
        json_data_obj = JsonData("data.json")
        print(f"Creating task: {task_name.text, task_deadline.text}")
        
        app.root.current_screen.ids["Container"].add_widget(ListItemWithCheckbox(text="[b]"+task_name.text+"[/b]", secondary_text=task_deadline.text))
        parent_list = app.root.current_screen.ids.ToDoListName.text.replace("[u]", "").replace("[/u]","").replace("[b]", "").replace("[/b]","")
        
        task_json = {"task_name":task_name.text, "completed":False, "task_date": task_deadline.text}
        json_data_obj.append_new_task(task_json, parent_list)
        
        task_name.text = ""
        task_deadline.text = ""

# Main screen for creating and managing list items 
class ToDoListPage(Screen):
    dialog = None
    #open edit task dialog 
    def open_edit_dialog(self, object):
        if not self.dialog: # if a dialog does not exits 
            self.dialog = MDDialog ( # define one 
                title="Edit Task",
                type="custom",
                content_cls=EditTaskDialogContent(object)
            )
        self.dialog.open() # open the dialog 
    # closes dialog box
    def close_dialog(self):
        self.dialog.dismiss()
        self.dialog = None
    # opens task creation dialog box 
    def show_task_dialog(self):
        if not self.dialog: # if a dialog does not exits 
            self.dialog = MDDialog ( # define one 
                title="Create Task",
                type="custom",
                content_cls=CreateTaskDialogContent()
            )
        self.dialog.open() # open the dialog 

    def edit_task():
        pass

    

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
        self.create_loaded_object(jsonDataObject.data["lists"][parent_list_index]["tasks"])
        
    def create_loaded_object(self, task_list):
        for i in task_list:
            loaded_task = ListItemWithCheckbox(text= "[b]" + i["task_name"] + "[/b]", secondary_text=i["task_date"])
            loaded_task.ids.check.active = i["completed"]
            if loaded_task.ids.check.active:
                loaded_task.text = "[s]" + loaded_task.text + "[/s]"
            self.ids["Container"].add_widget(loaded_task)
