from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen

listOfLists = []

class ToDoList():
    def __init__(self, _listName, _id):
        self.listName = _listName
        self.id = _id

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ToDoListCreation(MDScreen):
    dialog = None #Create a dialog variable for our dialog box
    screen_manager = ObjectProperty() #intansiate a screen manager for kv file
    def saveTask(self): #Function called when save button is pressed
        print("save button clicked") #TODO(TEMP) once feature finished remove this
        listname = self.ids.listNameField.text #take text from text field to useto create a task
        if len(listname) > 0: # check there is text in the text field
            newList = ToDoList(listname, len(listOfLists)) #create class for ToDo list
            listOfLists.append(newList) # add list to the list of lists
            viewScreen = self.screen_manager.get_screen('ToDoScreen') #use the screen manager to get the ToDo list viewer creen
            print(viewScreen.ids) #TODO idk why but this fooker is coming out empty every time it is called??? Find solution.... 
            self.screen_manager.current = 'ToDoScreen' # Changes screen to list view
        else: # if text input is empty
            if not self.dialog: #if there is no open dialog box
                self.dialog = MDDialog( #assign one 
                        text = "You have not entered a task name!",
                            buttons = [
                                MDFlatButton(
                                 text = "OKAY", on_release = self.close_dialog
                                 #TODO Change colour of the Okay text to Blue...
                                 )
                             ],
                         )
            self.dialog.open() #open popup
    def close_dialog(self,obj): #function to close pop up
        self.dialog.dismiss()

class ToDoScreen(MDScreen):
    screen_manager = ObjectProperty
    def __init__(self, **kwargs):
        super(ToDoScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        if len(listOfLists) == 0:
           noListLabel = MDLabel(text="You have not created a ToDo list, please use the '+' button to do so.", halign="center")
           self.add_widget(noListLabel)
        
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("ToDo.kv")


MainApp().run()
