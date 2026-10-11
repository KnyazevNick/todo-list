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

            check = self.check_id(self.utid)
            if check is not None:
                self.utid += 1
                return None
            
            self.utid += 1
            self.tasks.append(task_info)
            return task_info
        else:
            return None


    def check_id(self, utid: int):

        for task_info in self.tasks:
            if task_info['id'] == utid:
                return task_info
        return None
        
        
#new functions for api, db and other stuff
    def get_tasks(self, status = None):
        if status is None:
            return self.tasks
        else:
            tasks_filtered = []
            for task_info in self.tasks:
                if task_info['status'] == status:
                    tasks_filtered.append(task_info)

            return tasks_filtered

        


    def complete_task(self, task_id):
        """check id and if find return dict with status completed"""

        result = self.check_id(task_id)

        if result is None:
            return None

        if result['status'] == 'active':
            result['status'] = 'completed'

        return result


    def rewrite_task(self, task_id, new_text):
        result = self.check_id(task_id)

        if result is not None:
            result['task'] = new_text
            return result
        else:
            return None