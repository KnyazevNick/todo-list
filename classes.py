class TodoList():

    def __init__(self, tasks= []):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self):
        print('Choose task to delete:')
        count = 1

        for task in self.tasks:
            print(f'{count}-{task}')
            count += 1
        task_number = input('write number of the task: ')
        try:
            task_number = int(task_number) - 1
        except ValueError:
            print('please write number!')
            return None
        print(f'Are you sure want to delete {self.tasks[task_number]}')
        answer = input('y/n: ')
        if answer == 'y':
            removed_task = self.tasks.pop(task_number)
            print(f'successfuly deleted {removed_task}')
        elif answer == 'n':
            print('retry command')
            return None
        else:
            print('please answer y or n')
            return None
            

    def show_tasks(self):

        if self.tasks:
            for task in self.tasks:
                print(task)
        else:
            print('There are no tasks!')