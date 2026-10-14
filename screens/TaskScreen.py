from textual.containers import Horizontal, Vertical, Center, Middle
from textual.widgets import ListView,ListItem,Label,Input
from widgets.tasktable import TaskRow
from core.storage import load_tasks, add_task, delete_task, toggle_done, update_task
import json, os, tempfile

class TaskScreen(Vertical): 
    BINDINGS = [
    ("a", "add_task", "Add"),
    ("e", "edit_task", "Edit"),
    ("d", "delete_selected", "Delete Selected"),
    ("escape","cancel_edit","Cancel"),
    ("space","toggle_done","Toggle_done"),
    ]

    editing_task_id: str | None = None # stores the id for the thing we editing

    def compose(self):
        yield Input(placeholder="Add task here",id="task-input")
        yield ListView(id="task-list")
        
    def on_mount(self) -> None:
        self.run_worker(self.refresh_list())
        

    async def refresh_list(self):
        tasks = load_tasks()
        lv = self.query_one("#task-list", ListView)
        await lv.clear()
        if not tasks:
            lv.append(ListItem(Label("add a task it will not make you happier :) ")))
            return
        for task_id,task in tasks.items():
            row = Horizontal(
            Label("[]", classes="marker"),
            Label(f"{task_id:>3}", classes="task-id"),
            Label(task["title"], classes="task-title"),
            Label(f"{task.get('done', 0)}", classes="task-pomos"),
            classes="task-row",
            )
            lv.append(ListItem(row, id=f"task-{task_id}"))
                

    def set_active(self, task_id):
        for row in self.query(TaskRow):
            row.set_class(row.task_data.id == task_id, "active")

    def action_delete_selected(self): # use action_ prefix to work along side the BINDINGS it will call delete selected automatically but it needs the prefix
        lv = self.query_one("#task-list",ListView)
        item = lv.highlighted_child
        if item is None:
            return
        task_id = item.id.removeprefix("task-")
        delete_task(task_id)
        self.run_worker(self.refresh_list())
        
    def on_input_submitted(self,event: Input.Submitted)-> None: # when enter is pressed do :
        text = event.value # text its self
        if self.editing_task_id is None:
            if not text.strip():
                return
            add_task(text)
            event.input.value="" # set to nothing for next task input
            self.run_worker(self.refresh_list()) # refresh task list
        else:
            update_task(self.editing_task_id,title=event.value)
            self.editing_task_id = None
            event.input.placeholder = "New task..."
            self.run_worker(self.refresh_list())
    
    def action_edit_task(self):
        lv = self.query_one("#task-list",ListView)
        inp = self.query_one("#task-input", Input)
        item = lv.highlighted_child
        if item is None:
            return
        self.editing_task_id = item.id.removeprefix("task-")
        tasks = load_tasks()
        inp.value = tasks[self.editing_task_id]["title"]
        inp.focus()
        inp.placeholder = "Editing Task Press Enter to save"

    def action_cancel_edit(self):
        inp = self.query_one("#task-input", Input)
        lv = self.query_one("#task-list",ListView)
        inp.value = ""
        inp.placeholder = "New task..."
        self.editing_task_id = None
        lv.focus() # sets focus to the lis view

    def action_toggle_done(self):
        print("did i get called")
        lv = self.query_one("#task-list",ListView)
        item = lv.highlighted_child
        if item is None:
            return
        task_id = item.id.removeprefix("task-")
        toggle_done(task_id)
        self.run_worker(self.refresh_list())