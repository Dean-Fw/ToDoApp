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
    def save_data(self, new_list):
        with open(self.file_path, 'r+') as f:
            json_data = json.load(f)
            json_data["lists"].append(new_list)
            f.seek(0)
            json.dump(json_data, f, indent = 4)
     
def main():
    json_data_obj = JsonData("data.json")
    loaded_lists = json_data_obj.load_data()
    for i in loaded_lists:
        print(f"List Name: {i.list_name} \n Tasks:\n    {i.tasks}\n")
    new_list = {"list_name":"school tasks", "tasks":[{"task_name":"Do Homework","completed":False}]}
    json_data_obj.save_data(new_list)
    
main()

