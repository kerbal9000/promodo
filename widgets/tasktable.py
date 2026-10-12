from textual.widgets import ListItem, Checkbox, Label

class TaskRow(ListItem):
    def __init__(self, task):
        super().__init__()
        self.task_data = task

    def compose(self):
        with ListItem(id=f"task-{task_id}"):
            with Horizontal(classes="task-row"):

                yield Label("[*]" if task_id == active_id else "   ", classes="marker")
                yield Label(f"{task_id:>3}", classes="task-id")
                yield Label(task["title"], classes="task-title")
                yield Label(f"🍅 {task.get('done', 0)}/{task.get('est', 1)}", classes="task-pomos")


