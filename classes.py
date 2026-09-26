class TodoList():

    def __init__(self):
        self.tasks = []
        self.utid = 1000


    def add_task(self, task):
        if task.strip() != '':
            task_info = {
                'id' : self.utid,
                'task' : task,
                'status' : 'active',
            }

            self.utid += 1
            self.tasks.append(task_info)
            print(f'added task: {task}')
        else:
            print("you can't add empty task")
            return None


    def check_id(self, utid):
        if self.tasks:
            for task_info in self.tasks:
                if str(task_info['id']) == str(utid):
                    return task_info
        else:
            return None
                

    def remove_task(self):
        self.show_tasks()

        print('\nwhich task you want to delete?')
        answer = input('enter stop to cancel \n enter task id: ')
        if answer.lower().strip() != 'stop':
            info = self.check_id(answer)
            if info:
                answer = input(f'are you sure want to delete: {info['task']} (y/n): ')
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
        if self.tasks:
            check = False

            for task_info in self.tasks:
                if task_info['status'] == 'active':
                    print(f'\n\nid:\n{task_info['id']}')
                    print(f'task:\n{task_info['task']}')
                    print(f'status:\n{task_info['status']}')
                    check = True
            if check:
                print('\nwhich task you want to mark as completed?')
                answer = input('enter stop to cancel \n enter task id: ')
                if answer.lower().strip() != 'stop':
                    info = self.check_id(answer)
                    if info:
                        pass
                    else:
                        print('id not found')
                        return None
                    
                    if info['status'] == 'active':
                        answer = input(f'are you sure want to mark as completed: {info['task']} (y/n): ')
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

            else:
                print('there are no active tasks')

        else:
            print('todolist is empty!')
            return None


    def update_task(self):
        self.show_tasks()

        print('\nwhich task you want to update?')
        answer = input('enter stop to cancel \n enter task id: ')
        if answer.lower().strip() != 'stop':
            info = self.check_id(answer)
            if info:
                answer = input(f'are you sure want to rewrite: {info['task']} (y/n): ')
                if answer.lower().strip() == 'y':

                    update = input('Write new task: ')
                    if update.strip() != '':
                        info['task'] = update
                        print('updated task!')
                    else:
                        print("if you want to delete task use command: remove_task")
                        return None
                    
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