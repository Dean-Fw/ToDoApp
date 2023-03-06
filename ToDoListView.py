from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from ToDoListPages import CreatedToDoListPage, LoadedToDoListPage
from JSON_Interface import JsonData
from kivy.clock import Clock
from functools import partial
from DialogBoxes import CreateListDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from ListItems import ListCard

class ToDoListView(MDScreen):
    def __init__(self,**kw):
        super().__init__(**kw)
        Clock.schedule_once(partial(self.load_lists)) 
        self.screen_manager = ObjectProperty()
    ''' Methods for loading tasks from JSON file to screen'''
    def load_lists(self, *largs):
        json_data_object = JsonData("data.json")
        self.loaded_items = []

        for i in json_data_object.data["lists"]: 
            self.add_loaded_item_to_list(i)    

        for i in self.loaded_items:
            self.bind_on_release_to_loaded_item(i) 

    def bind_on_release_to_loaded_item(self, loaded_item):
        self.screen_manager.add_widget(LoadedToDoListPage(self.screen_manager, name = loaded_item.text))
        loaded_item.bind(on_release= lambda x: self.change_screen(loaded_item.text))
    
    def add_loaded_item_to_list(self, loaded_item):
            loaded_object = ListItemWithoutCheckbox(self.screen_manager, text="[b]" + loaded_item["list_name"] + "[/b]")
            self.ids["Container"].add_widget(loaded_object)
            self.loaded_items.append(loaded_object)
            self.add_loaded_item_to_home_screen(loaded_item, loaded_object)
    
    def add_loaded_item_to_home_screen(self, loaded_item, loaded_object):
        if loaded_item["favourited"]:
            loaded_object.add_favourited_list_to_home()
            loaded_object.ids.star.icon = "star"
        return


    '''Methods for Opening and closing dialog boxes'''
    task_list_dialog = None
    # Opens Dialog box that allows for the creation of classes 
    def show_task_dialog(self,screen_manager): 
        if not self.task_list_dialog: # if a dialog does not exits 
            self.task_list_dialog = MDDialog ( # define one 
                title="Create a ToDo list",
                type="custom",
                content_cls=CreateListDialog(screen_manager)
            )
        self.task_list_dialog.open() # open the dialog 

    # Closes dialog box 
    def close_dialog(self):
        self.task_list_dialog.dismiss()

    # Takes values returned from dialog box and adds it to the screen,
    # also creates a screen for the item and adds it to the screen manager
    def add_task(self, task):
        print(f"Creating list: {task.text}")
        list_without_checkbox = ListItemWithoutCheckbox(self.screen_manager,text="[b]" + task.text + "[/b]")
        
        json_data_obj = JsonData("data.json")
        json_data_obj.append_new_list({"list_name": task.text, "favourited": False, "tasks": []})
        
        self.create_screen(list_without_checkbox)
       
        task.text = "" 
    
    # Allows for the changing of screens when a list item is pressed
    def change_screen(self, list_name):
        app = MDApp.get_running_app()
        app.root.ids.topBar.title = list_name 
        self.screen_manager.get_screen(list_name).previous = "ToDoListFeature"
        self.screen_manager.current = list_name
        print(f"Changing screen to: {self.screen_manager.current}")

    def create_screen(self, object):
        self.screen_manager.add_widget(CreatedToDoListPage(name=str(object.text)))
        object.bind(on_release= lambda x : self.change_screen(object.text))
        self.ids["Container"].add_widget(object)

'''List object'''
# This class can not be placed inside of the LitsItems.py file as it causes circular imports
class ListItemWithoutCheckbox(OneLineAvatarIconListItem):

    def __init__(self, screen_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager = screen_manager

    def favourite_list(self):
        self.change_star_state()
    
    # change the icon that marks whether a list has been favourited or not 
    def change_star_state(self):
        if self.ids.star.icon == "star-outline":
            self.ids.star.icon = "star"
            self.add_favourited_list_to_home()
        else:
            self.ids.star.icon = "star-outline"
            self.remove_favourited_list_from_home()
        self.save_favourite_to_Json()

    def create_card_for_favourited_list(self):
        list_details = self.find_list_details_in_Json()
        list_card = ListCard()
        list_card.id = self.text.replace("[b]", "").replace("[/b]", "")
        list_card.ids.list_name.text = self.text
        list_card.ids.list_count.text = "[i]Total Tasks : " + str(list_details["list_length"]) + "[/i]"
        list_card.ids.total_complete.text = "[i]Total Tasks completed : " + str(list_details["total_complete"]) + "[/i]"
        return list_card

    def add_favourited_list_to_home(self):
        app = MDApp.get_running_app()
        list_card = self.create_card_for_favourited_list()
        for child in app.root.ids.screen_manager.get_screen("HomeScreen").ids.home_list.children:
            if "FavouriteSpace" in str(child):
                child.ids.space_for_cards.add_widget(list_card)
                child.height = child.calc_height()
                child.check_if_empty()

    def remove_favourited_list_from_home(self):
        card_id = self.text.replace("[b]","").replace("[/b]","")
        favourite_space = self.find_favourite_space_object()
        for child2 in favourite_space.ids.space_for_cards.children:
            if child2.id == card_id:
                favourite_space.ids.space_for_cards.remove_widget(child2)
                favourite_space.height = favourite_space.calc_height()
        favourite_space.check_if_empty()

    def find_favourite_space_object(self):
        app = MDApp.get_running_app()
        for child in app.root.ids.screen_manager.get_screen("HomeScreen").ids.home_list.children:
            if "FavouriteSpace" in str(child):
                return child
    
    def find_list_details_in_Json(self):
        json_data_obj = JsonData("data.json")
        json_details = {}
        list_index = json_data_obj.find_list(self.text.replace("[b]","").replace("[/b]",""))
        list_total_complete = self.find_total_completed_tasks(json_data_obj, list_index)
        json_details["list_length"] = len(json_data_obj.data["lists"][list_index]["tasks"])
        json_details["total_complete"] = list_total_complete
        return json_details
    
    def find_total_completed_tasks(self, json_data_obj, list_index):
        list_total_complete = 0
        for task in json_data_obj.data["lists"][list_index]["tasks"]:
            if task["completed"]:
                list_total_complete += 1
        return list_total_complete

    def save_favourite_to_Json(self):
        json_data_obj = JsonData("data.json")
        json_data_obj.edit_favourite(self.text.replace("[b]","").replace("[/b]",""))

    # Allows for the deletion of items upon clicking the "bin" icon
    def delete_item(self):
        # Remove screen from app
        app = MDApp.get_running_app() # create instance of running app
        self.parent.remove_widget(self) # remove item from the list 
        print(f"Removing Screen: {self.text}")
        # Remove List from JSON file 
        json_data_obj = JsonData("data.json")

        json_data_obj.remove_list(self.text.replace("[b]", "").replace("[/b]",""))
        app.root.ids.screen_manager.remove_widget(CreatedToDoListPage(name=self.text)) # delete the screen

