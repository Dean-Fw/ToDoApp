from JSON_Interface import JsonData

#example
def main():
    json_data_obj = JsonData("data.json")
    
    #json_data_obj.remove_list("school tasks")
    #new_list = {"list_name":"school tasks", "tasks":[{"task_name":"Do Homework","completed":False}]}
    #json_data_obj.append_new_list(new_list) 

    new_task = {"task_name": "do laundry", "completed": False}
    #json_data_obj.append_new_task(new_task, "home tasks")
    #json_data_obj.complete_task("do laundry", "home tasks")
    
    #json_data_obj.remove_task("do laundry", "home tasks")

main()

