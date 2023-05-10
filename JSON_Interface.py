import json

# method to open and load data from a JSON file        
class JsonData:
    
    def __init__(self, FilePath):
        self.file_path = FilePath
        self.data = self.open_and_load_JSON()
    
    '''file based methods'''
    def open_and_load_JSON(self):
        try:
            f = open(self.file_path)
            print("--- JSON FILE OPENED ---\n")
            data = json.load(f)
            print("--- JSON FILE LOADED ---\n")
            f.close()
            print("--- JSON FILE CLOSED ---\n")
            return data
        except:
            print("ERROR: Could not open JSON file")
            exit()
       
    def save_changes(self, type_of_change):
            with open(self.file_path, type_of_change) as f:
                print("--- JSON FILE SAVED ---")
                f.seek(0)
                json.dump(self.data, f, indent = 4)
                f.flush()
    
   
    '''file appending methods'''
    def append_new_card(self, position,new_list):
        self.data["screens"][position]["cards"].append(new_list)
        self.save_changes("r+")
    
    def append_new_screen(self,new_screen):
        self.data["screens"].append(new_screen)
        self.save_changes("r+")
    
    def append_new_task(self, screen_name, list_name, new_task):
        screen_index = self.find_screen_index(screen_name)
        list_index = self.find_list_index(screen_index, list_name)
        self.data["screens"][screen_index]["cards"][list_index]["content"]["list_items"].append(new_task)
        self.save_changes("r+")

    '''editing methods'''
    def edit_task(self,screen_name,list_name,task_name, new_task):
        screen_index = self.find_screen_index(screen_name)
        list_index = self.find_list_index(screen_index, list_name)
        task_index = self.find_task_index(screen_index, list_index,task_name)
        self.data["screens"][screen_index]["cards"][list_index]["content"]["list_items"][task_index] = new_task
        self.save_changes("w")

    def edit_list(self, screen_name, list_name, new_list):
        screen_index = self.find_screen_index(screen_name)
        list_index = self.find_list_index(screen_index, list_name)
        print(list_index)
        self.data["screens"][screen_index]["cards"][list_index]["content"]["list_name"] = new_list
        self.save_changes("w")
    
    def edit_image(self,screen_name,image_name,new_image):
        screen_index = self.find_screen_index(screen_name)
        image_index = self.find_image_index(screen_index, image_name)
        self.data["screens"][screen_index]["cards"][image_index]["content"] = new_image
        self.save_changes("w")

    def edit_note(self,screen_name,note_name,new_note):
        screen_index = self.find_screen_index(screen_name)
        note_index = self.find_note_index(screen_index, note_name)
        self.data["screens"][screen_index]["cards"][note_index]["content"] = new_note

        self.save_changes("w")

    '''deletion methods'''
    def remove_note(self, screen_name, note_name):
        screen_index = self.find_screen_index(screen_name)
        note_index = self.find_note_index(screen_index, note_name)
        del self.data["screens"][screen_index]["cards"][note_index]

        self.save_changes("w")
    
    def remove_list(self, screen_name, list_name):
        screen_index = self.find_screen_index(screen_name)
        list_index = self.find_list_index(screen_index, list_name)
        del self.data["screens"][screen_index]["cards"][list_index]

        self.save_changes("w")

    def remove_image(self, screen_name, image_name):
        screen_index = self.find_screen_index(screen_name)
        image_index = self.find_image_index(screen_index, image_name)
        del self.data["screens"][screen_index]["cards"][image_index]

        self.save_changes("w")

    def remove_task(self, screen_name, list_name, task_name):
        screen_index = self.find_screen_index(screen_name)
        list_index = self.find_list_index(screen_index,list_name)
        task_index = self.find_task_index(screen_index, list_index, task_name)
        del self.data["screens"][screen_index]["cards"][list_index]["content"]["list_items"][task_index]

        self.save_changes("w")
    
    
    '''search methods'''
    def find_note_index(self,screen_index,target_note_name):
        for i in self.data["screens"][screen_index]["cards"]:
            if i["type"] == "note" and i["content"]["note_title"] == target_note_name:
                return self.data["screens"][screen_index]["cards"].index(i)

    def find_list_index(self, screen_index ,target_list_name):
        for i in self.data["screens"][screen_index]["cards"]:
            if i["type"] == "list" and i["content"]["list_name"] == target_list_name:
                return self.data["screens"][screen_index]["cards"].index(i)

    def find_image_index(self, screen_index, target_image_name):
        for i in self.data["screens"][screen_index]["cards"]:
            if i["type"] == "image" and i["content"]["name"] == target_image_name:
                return self.data["screens"][screen_index]["cards"].index(i)

    def find_screen_index(self, screen_name):
        for i in self.data["screens"]:
            if screen_name == i["name"]:
                return self.data["screens"].index(i)
    
    def find_task_index(self, screen_index, list_index, task_name):
        for i in self.data["screens"][screen_index]["cards"][list_index]["content"]["list_items"]:
            if task_name == i["task_name"]:
                return self.data["screens"][screen_index]["cards"][list_index]["content"]["list_items"].index(i)
    
    
    
    '''OLD STUFF'''
    '''search methods'''
    # find lists in JSON file
    def find_list(self, target_list_name):
        index = 0
        for i in self.data["lists"]:
            if i["list_name"] == target_list_name:
                return index
            index += 1    
    # find tasks from a given parent list in JSON file
    def find_task(self, target_task, index_of_parent_list):
        index = 0
        for i in self.data["lists"][index_of_parent_list]["tasks"]:
            if i["task_name"] == target_task:
                return index
            index += 1
    
    '''List based methods'''
    # create a new list and add to JSON file
    def append_new_list(self, new_list):
        self.data["lists"].append(new_list)
        self.save_changes("r+")
    # find list in JSON, remove it and update the file 
    #def remove_list(self, list_name):
    #    list_index = self.find_list(list_name)
    #    del self.data["lists"][list_index]
    #    self.save_changes("w")
    # find list in JSON, adjust it's "favourited" property
    def edit_favourite(self, list_name):
        list_index = self.find_list(list_name)
        if self.data["lists"][list_index]["favourited"]:
            self.data["lists"][list_index]["favourited"] = False
        else:
            self.data["lists"][list_index]["favourited"] = True
        self.save_changes("w")
    '''Task based methods'''
    # find list in JSON, append to it's task object
    #def append_new_task(self, new_task, parent_list):
    #    parent_list_index = self.find_list(parent_list)
    #    self.data["lists"][parent_list_index]["tasks"].append(new_task)
    #    self.save_changes("w")
    # find task and swap its completed status 
    def complete_task(self, task_to_complete, parent_list):
        parent_list_index = self.find_list(parent_list)
        task_index = self.find_task(task_to_complete, parent_list_index)
        if self.data["lists"][parent_list_index]["tasks"][task_index]["completed"] == False:
            self.data["lists"][parent_list_index]["tasks"][task_index]["completed"] = True
        else:
            self.data["lists"][parent_list_index]["tasks"][task_index]["completed"] = False
        self.save_changes("w")
    # find and remove tasks from a list, then save to JSON 
    #def remove_task(self, task_to_remove, parent_list):
    #    parent_list_index = self.find_list(parent_list)
    #    task_index = self.find_task(task_to_remove, parent_list_index)
    #    del self.data["lists"][parent_list_index]["tasks"][task_index]
    #    self.save_changes("w")
    # find and edit task in list, then save to JSON
    #def edit_task(self, new_data ,task_to_edit, parent_list):
    #    parent_list_index = self.find_list(parent_list)
    #    task_index = self.find_task(task_to_edit, parent_list_index)
    #
    #    self.data["lists"][parent_list_index]["tasks"][task_index]["task_name"] = new_data[0]
    #    self.data["lists"][parent_list_index]["tasks"][task_index]["task_date"] = new_data[1]
    #    self.save_changes("w")