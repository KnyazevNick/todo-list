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

    def check_id(self, utid):
        if self.tasks:
            for task_info in self.tasks:
                info = task_info
                for id in task_info.values():
                    if str(id) == utid:
                        return info
        else:
            return None

    def print_list(self):
        if self.tasks:

            for task_info in self.tasks:
                print(f'id:{task_info['id']} - {task_info['task']}')
        else:
            print('todo list is empty!')
                

    def remove_task(self):
        self.print_list()

        print('\nwhich task you want to delete?')
        answer = input('enter stop to cancel \n enter task id: ')
        if answer.lower().strip() != 'stop':
            info = self.check_id(answer)
            if info:
                answer = input(f'are you sure want to delete {info['task']} (y/n): ')
                if answer.lower().strip() == 'y':
                    self.tasks.remove(info)
                    print('removed task!')
                elif answer.lower().strip() == 'n':
                    return None
                else:
                    print('please answer "y" or "n"')
                    return None
            else:
                print("id wasn't found")
                return None
        else:
            return None


    def update_task(self):
        self.print_list()
        print('\nwhich task you want to update?')
        answer = input('enter stop to cancel \n enter task id: ')
        if answer.lower().strip() != 'stop':
            info = self.check_id(answer)
            if info:
                answer = input(f'are you sure want to rewrite {info['task']} (y/n): ')
                if answer.lower().strip() == 'y':
                    update = input('Write new task: ')
                    info['task'] = update
                    print('updated task!')
                elif answer.lower().strip() == 'n':
                    return None
                else:
                    print('please answer "y" or "n"')
                    return None
            else:
                print("id wasn't found")
                return None
        else:
            return None


    def show_tasks(self):

        if self.tasks:
            for task_info in self.tasks:
                print(f'id:{task_info['id']} - task: {task_info['task']}')
        else:
            print('There are no tasks!')