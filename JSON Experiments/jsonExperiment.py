import json

class ToDoList:
    def __init__(self, ListName, Tasks):
        self.list_name = ListName
        self.tasks = Tasks
    
    def print_data(self):
        print(f"List Name: {self.list_name}\n Tasks: \n     {self.tasks}\n")
        
def open_and_load_JSON():
    try:
        f = open("data.json")
        print("--- JSON FILE OPENED ---\n")
        data = json.load(f)
        print("--- JSON FILE LOADED ---\n")
        f.close()
        print("--- JSON FILE CLOSED ---\n")
        return data
    except:
        print("ERROR: Could not open JSON file")
        exit()

def main():
    data = open_and_load_JSON()
    ToDoLists = []
    
    for i in data["lists"]:
        new_list = ToDoList(i["list_name"],i["tasks"])
        ToDoLists.append(new_list)
  
    for i in ToDoLists:
        i.print_data()

main()

