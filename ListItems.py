from JSON_Interface import JsonData
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, screen_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager = screen_manager
    # Allows users to complete tasks and see them crossed out 
    def mark(self, check, list_item):
        ScreenObject = self.screen_manager.current_screen # This is almost the ugliest most stupidest most dumbest solution, but it's all i got :/
        if check.active == True: # when a checkbox is ticked
            list_item.text = "[s]"+list_item.text+"[/s]" # add strike through format to completed tasks
        else:
            list_item.text = list_item.text.replace("[s]", "").replace("[/s]","") # remove strike through markup
        
        json_data_obj = JsonData("data.json")
        json_data_obj.complete_task(list_item.text.replace("[b]", "").replace("[/b]", "").replace("[s]", "").replace("[/s]",""), ScreenObject.name.replace("[b]", "").replace("[/b]", ""))
        self.screen_manager.current_screen.adjust_home_screen_content(json_data_obj, "Complete")
    # Allows for the deletion of item upon clcking the "bin icon"
    def delete_item(self, list_item):
        ScreenObject = self.screen_manager.current_screen # This is almost the ugliest most stupidest most dumbest solution, but it's all i got :/

        json_data_obj = JsonData("data.json")
        print(ScreenObject.name)
        json_data_obj.remove_task(list_item.text.replace("[b]", "").replace("[/b]", "").replace("[s]", "").replace("[/s]",""), ScreenObject.name.replace("[b]", "").replace("[/b]", ""))

        print(f"Deleting item: {list_item.text}")
        self.parent.remove_widget(list_item)

        self.screen_manager.current_screen.adjust_home_screen_content(json_data_obj, "Length")
        
# Checkbox for list items 
class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

class ListCard(MDBoxLayout):
    pass

