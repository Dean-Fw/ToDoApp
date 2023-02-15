import json

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
        length = len(self.data["lists"])
        print(f"total len of lists thing: {length}")
        count = 0
        for i in self.data["lists"]:
            print(i)
            if i["list_name"] == list_name:                
                del self.data["lists"][count]
                break
            count += 1
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

    #new_task = {"task_name": "do laundry", "completed": False}
    #json_data_obj.append_new_task(new_task, "home tasks")
    
    #json_data_obj.remove_task("do laundry", "home tasks")

    
    
    
   
   

main()

