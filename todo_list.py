from pathlib import Path
import json
from classes import TodoList



todo_list = TodoList()

path = Path(__file__).parent / 'todolist.json'
if path.exists():
    contents = path.read_text()
    id_and_tasks = json.loads(contents)
    todo_list.tasks = id_and_tasks['tasks']
    todo_list.utid = id_and_tasks['next_id']

def save_json():
    contents = json.dumps({'tasks' : todo_list.tasks, 'next_id' : todo_list.utid})
    path.write_text(contents)


while True:
    print('===MENU===')
    print('write what you want to do')
    print('write help to see commands')
    command = input('command: ')

    if command == 'help':
        print('show_tasks - print todo-list')
        print('add_task - add task to todo-list')
        print('update_task - update task in the todo-list')
        print('remove_task - remove task from the todo-list')
        print('quit - end program')

    elif command == 'show_tasks':
        todo_list.show_tasks()

    elif command == 'add_task':
        task = input('write task: ')
        todo_list.add_task(task)
        print(f'added {task}')
        save_json()

    elif command == 'update_task':
        todo_list.update_task()
        save_json()

    elif command == 'remove_task':
        todo_list.remove_task()
        save_json()

    elif command == 'quit':
        break

    else:
        print(f'ERROR - unknown command: {command}')

save_json()