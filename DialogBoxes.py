from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp
from JSON_Interface import JsonData
from functools import partial
from kivymd.uix.button import MDRaisedButton
from ListItems import ListItemWithCheckbox

# Rule for save button used in edit dialog
class SaveEditedTaskButton(MDRaisedButton):
    pass

# Rule for save button used in task creation dialog 
class SaveNewTaskButton(MDRaisedButton):
    pass

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
        self.ids.task_text.text =  task_name.replace("[b]", "").replace("[/b]", "").replace("[s]","").replace("[/s]","")
        self.ids.date_text.text = task_date
        self.ids.save_or_exit.add_widget(SaveEditedTaskButton())
         
    def edit_task(self):
        self.edit_JSON([self.ids.task_text.text, self.ids.date_text.text])
        self.parent_item.text = "[b]" + self.ids.task_text.text + "[/b]"
        self.parent_item.secondary_text = self.ids.date_text.text

    def edit_JSON(self, new_task_data):
        app = MDApp.get_running_app()
        json_data_obj = JsonData("data.json")
        parent_list_name = app.root.ids.screen_manager.current_screen.name.replace("[b]","").replace("[/b]","")
        task_name = self.parent_item.text.replace("[b]", "").replace("[/b]", "").replace("[s]","").replace("[/s]","")
        json_data_obj.edit_task(new_task_data, task_name, parent_list_name)
        
# child of dialog content to allow for creation of tasks 
class CreateTaskDialogContent(DialogContent):
    def __init__(self,screen_manager,**kwargs):
        super().__init__(**kwargs) 
        self.ids.date_text.text = str("")
        self.ids.save_or_exit.add_widget(SaveNewTaskButton())
        self.screen_manager = screen_manager
    
    def add_task(self):
        task_name = self.ids.task_text
        task_deadline = self.ids.date_text
        
        json_data_obj = JsonData("data.json")
        print(f"Creating task: {task_name.text, task_deadline.text}")

        self.screen_manager.current_screen.ids["Container"].add_widget(ListItemWithCheckbox(self.screen_manager, text="[b]"+task_name.text+"[/b]", secondary_text=task_deadline.text))
        parent_list = self.screen_manager.current_screen.name.replace("[b]", "").replace("[/b]","")
        
        task_json = {"task_name":task_name.text, "completed":False, "task_date": task_deadline.text}
        json_data_obj.append_new_task(task_json, parent_list)
        
        task_name.text = ""
        task_deadline.text = ""
        
        self.screen_manager.current_screen.adjust_home_screen_content(json_data_obj, "Length")

class CreateListDialog(MDBoxLayout):
    def __init__(self, screen_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager = screen_manager