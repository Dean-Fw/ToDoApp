from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime

'''Code for Creation and viewing of multiple ToDoLists'''

class ToDoListView(Screen):
    task_list_dialog = None
    def show_task_dialog(self):
        if not self.task_list_dialog: # if a dialog does not exits 
            self.task_list_dialog = MDDialog ( # define one 
                title="Create a ToDo list",
                type="custom",
                content_cls=CreateListDialog()
            )
        self.task_list_dialog.open() # open the dialog 
    
    def close_dialog(self):
        self.task_list_dialog.dismiss()

    def add_task(self, task):
        print(task.text)
        self.parent.add_widget(ToDoListPage(name=str(task.text)))
        self.ids["Container"].add_widget(ListItemWithoutCheckbox(text="[b]" + task.text + "[/b]",))
        task.text = ""
    
    def change_screen(self, list_name):
        self.parent.current = list_name


class ListItemWithoutCheckbox(OneLineAvatarIconListItem):
    def delete_item(self, list_item):
        self.parent.remove_widget(list_item)

class CreateListDialog(MDBoxLayout):
    pass

'''Code For Individual ToDo List pages'''

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def mark(self, check, list_item):
        if check.active == True: # when a checkbox is ticked
            list_item.text = "[s]"+list_item.text+"[/s]" # add strike through format to completed tasks
        else:
            list_item.text = list_item.text.replace("[s]", "").replace("[/s]","") # remove strike through markup
    
    def delete_item(self, list_item):
        self.parent.remove_widget(list_item)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

class DialogContent(MDBoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str("") # set date text to todays date when user 
        # %A = Week Day, %d = Day, %B = Month name, %Y = Year
    def show_date_picker(self):
        date_dialog = MDDatePicker() #instantiate date picker widget
        date_dialog.bind(on_save=self.on_save) #bind the date picker to a function that saves content
        date_dialog.open() # open the dialog 

    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)
    
class ToDoListPage(Screen):
    task_list_dialog = None
    def show_task_dialog(self):
        if not self.task_list_dialog: # if a dialog does not exits 
            self.task_list_dialog = MDDialog ( # define one 
                title="Create Task",
                type="custom",
                content_cls=DialogContent()
            )
        self.task_list_dialog.open() # open the dialog 
    
    def close_dialog(self):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        print(task.text, task_date.text)
        self.ids["Container"].add_widget(ListItemWithCheckbox(text="[b]"+task.text+"[/b]", secondary_text=task_date.text))
        task.text = ""
        task_date.text = ""

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