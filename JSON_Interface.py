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
    def remove_list(self, list_name):
        list_index = self.find_list(list_name)
        del self.data["lists"][list_index]
        self.save_changes("w")
    
    '''Task based methods'''
    # find list in JSON, append to it's task object
    def append_new_task(self, new_task, parent_list):
        parent_list_index = self.find_list(parent_list)
        self.data["lists"][parent_list_index]["tasks"].append(new_task)
        self.save_changes("w")
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
    def remove_task(self, task_to_remove, parent_list):
        parent_list_index = self.find_list(parent_list)
        task_index = self.find_task(task_to_remove, parent_list_index)
        del self.data["lists"][parent_list_index]["tasks"][task_index]
        self.save_changes("w")
