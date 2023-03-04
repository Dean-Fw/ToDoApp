from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from JSON_Interface import JsonData
from functools import partial
from kivy.clock import Clock
from DialogBoxes import EditTaskDialogContent, CreateTaskDialogContent
from ListItems import ListItemWithCheckbox
from kivymd.app import MDApp

# Main screen for creating and managing list items 
class CreatedToDoListPage(Screen):      
    # variable to hold dialog object 
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
    # opens task creation dialog box 
    def show_task_dialog(self, screen_manager):
        if not self.dialog: # if a dialog does not exits 
            self.dialog = MDDialog ( # define one 
                title="Create Task",
                type="custom",
                content_cls=CreateTaskDialogContent(screen_manager)
            )
        self.dialog.open() # open the dialog 
    # closes dialog box
    def close_dialog(self):
        self.dialog.dismiss()
        self.dialog = None

    def adjust_home_screen_content(self, json_data_obj):
        parent_list = self.find_parent_list()
        is_list_favourited = self.check_if_list_is_favourited(parent_list)
        parent_list_index = json_data_obj.find_list(parent_list.text.replace("[b]","").replace("[/b]",""))
        if is_list_favourited:
            for child in self.screen_manager.get_screen("HomeScreen").ids.home_list.children:
                if child.id == parent_list.text.replace("[b]","").replace("[/b]",""):
                    child.ids.list_count.text = "[i]Total Tasks : "+ str(len(json_data_obj.data["lists"][parent_list_index]["tasks"])) +"[/i]"

    def find_parent_list(self):
        parent_list_name = self.screen_manager.current_screen.name
        for list_item in self.screen_manager.get_screen("ToDoListFeature").ids["Container"].children:
            if list_item.text == parent_list_name:
                return list_item
    
    def check_if_list_is_favourited(self, parent_list):
        if parent_list.ids.star.icon == "star":
            return True
        return False

# child class of ToDoListPage for use when loading in pages from JSON file
class LoadedToDoListPage(CreatedToDoListPage):
    def __init__(self,screen_manager,**kw):
        super().__init__(**kw)
        Clock.schedule_once(partial(self.load_tasks))
        self.screen_manager = screen_manager
    # load tasks from JSON file and place in list object
    def load_tasks(self, *largs):
        app = MDApp.get_running_app()
        jsonDataObject = JsonData("data.json")
        print(self.name)
        parent_list_index = jsonDataObject.find_list(self.name.replace("[b]", "").replace("[/b]", ""))
        print(f"Parent list index: {parent_list_index}")
        self.create_loaded_object(jsonDataObject.data["lists"][parent_list_index]["tasks"])
    # create a list item object and add it to the screen's list object  
    def create_loaded_object(self, task_list):
        for i in task_list:
            loaded_task = ListItemWithCheckbox(self.screen_manager, text= "[b]" + i["task_name"] + "[/b]", secondary_text=i["task_date"])
            loaded_task.ids.check.active = i["completed"]
            if loaded_task.ids.check.active:
                loaded_task.text = "[s]" + loaded_task.text + "[/s]"
            self.ids["Container"].add_widget(loaded_task)
