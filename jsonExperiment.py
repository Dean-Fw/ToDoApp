import json

# class to store and display data for a todo list object
class ToDoList:
    
    def __init__(self, ListName, Tasks):
        self.list_name = ListName
        self.tasks = Tasks
    
    def print_data(self):
        print(f"List Name: {self.list_name}\n Tasks: \n     {self.tasks}\n")

# method to open and load data from a JSON file        
class JsonData:
    
    def __init__(self, FilePath):
        self.file_path = FilePath
        self.data = self.open_and_load_JSON()
    
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
    
    def load_data(self):
        ToDo_lists = []
        for i in self.data["lists"]:
            saved_list = ToDoList(i["list_name"],i["tasks"])
            ToDo_lists.append(saved_list)
        return ToDo_lists
    
    def save_changes(self, type_of_change):
            with open(self.file_path, type_of_change) as f:
                f.seek(0)
                json.dump(self.data, f, indent = 4)
                f.flush()
    
    def append_new_list(self, new_list):
        self.data["lists"].append(new_list)
        self.save_changes("r+")
        self.data = self.open_and_load_JSON()

    def remove_list(self, list_name):
        for i in range(len(self.data["lists"])):
            if self.data["lists"][i]["list_name"] == list_name:
                del self.data["lists"][i]
        self.save_changes("w")

    def append_new_task(self, new_task, parent_list):
        for i in range(len(self.data["lists"])):
            if self.data["lists"][i]["list_name"] == parent_list:
                print(f"Parent list found: {parent_list}")
                self.data["lists"][i]["tasks"].append(new_task)
            else:
                print(f"list not found: {parent_list}")
        self.save_changes("w")
        self.data = self.open_and_load_JSON()

    def remove_task(self, task_to_remove, parent_list):
        for i in range(len(self.data["lists"])):
            if self.data["lists"][i]["list_name"] == parent_list:
                for j in range(len(self.data["lists"][i]["tasks"])):
                    if self.data["lists"][i]["tasks"][j]["task_name"] == task_to_remove:
                        del self.data["lists"][i]["tasks"][j]
        self.save_changes("w")

def main():
    json_data_obj = JsonData("data.json")
    
    #json_data_obj.remove_list("school tasks")
    #new_list = {"list_name":"school tasks", "tasks":[{"task_name":"Do Homework","completed":False}]}
    #json_data_obj.append_new_list(new_list) 

    new_task = {"task_name": "do laundry", "completed": False}
    json_data_obj.append_new_task(new_task, "home tasks")
    
    #json_data_obj.remove_task("do laundry", "home tasks")
    
    loaded_lists = json_data_obj.load_data()
     
    for i in loaded_lists:
        print(f"List Name: {i.list_name} \n Tasks:\n    {i.tasks}\n")
    
    
    
   
   

main()

