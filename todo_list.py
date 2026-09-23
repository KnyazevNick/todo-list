todo_list = []

def add_task(tasks, task):
    tasks.append(task)

def show_tasks(tasks):
    if tasks:
        for task in tasks:
            print(task)
    else:
        print('There are no tasks!')


while True:
    print('===MENU===')
    print('write what you want to do')
    print('write help to see commands')
    command = input('command: ')

    if command == 'help':
        print('show_tasks - print todo-list')
        print('add_task - add task to todo-list')
        print('quit - end program')

    elif command == 'show_tasks':
        show_tasks(todo_list)

    elif command == 'add_task':
        task = input('write task: ')
        add_task(todo_list, task)

    elif command == 'quit':
        break

    else:
        print(f'ERROR - unknown command:{command}')

