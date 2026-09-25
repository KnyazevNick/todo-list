class TodoList():

    def __init__(self, tasks= []):
        self.tasks = []
        self.utid = 1000


    def add_task(self, task):

        task_info = {
            'id' : self.utid,
            'task' : task,
        }

        self.utid += 1
        self.tasks.append(task_info)


    def remove_task(self):
        pass


    def update_task(self):
        pass


    def show_tasks(self):

        if self.tasks:
            for task in self.tasks:
                print(task)
        else:
            print('There are no tasks!')