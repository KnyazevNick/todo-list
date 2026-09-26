class TodoList():

    def __init__(self, tasks= []):
        self.tasks = []
        self.utid = 1000


    def add_task(self, task):

        task_info = {
            'id' : self.utid,
            'task' : task,
            'status' : 'active',
        }

        self.utid += 1
        self.tasks.append(task_info)

    def check_id(self, utid):
        if self.tasks:
            for task_info in self.tasks:
                if str(task_info['id']) == str(utid):
                    return task_info
        else:
            return None

    def print_list(self):
        if self.tasks:

            for task_info in self.tasks:
                print(f'id:{task_info['id']} - {task_info['task']}')
        else:
            print('todo list is empty!')
            return None
                

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

    def complete_task(self):
        self.print_list()
        print('\nwhich task you want to mark as completed?')
        answer = input('enter stop to cancel \n enter task id: ')
        if answer.lower().strip() != 'stop':
            info = self.check_id(answer)
            if info:
                answer = input(f'are you sure want to mark as completed {info['task']} (y/n): ')
                if answer.lower().strip() == 'y':
                    info['status'] = 'completed'
                    print('congratulations with the completed task!')
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
                print(f'\n\nid:\n{task_info['id']}')
                print(f'task:\n{task_info['task']}')
                print(f'status:\n{task_info['status']}')
        else:
            print('There are no tasks!')