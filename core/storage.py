path_to_json = "storage/task.json"#needs to be changed to a proper directory make python make one
import json,tempfile,os

def load_tasks():
    return load_data()["tasks"]

def load_data():
    try:
        with open(path_to_json) as f:
            raw = f.read()
            data = json.loads(raw)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"tasks": {}, "next_id": 1}

def save_data(data, path=path_to_json): # saves data if file closes unexpectadly
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)

def add_task(title,priority=3,done=False):
    data = load_data()
    task_id = str(data["next_id"])
    data["tasks"][task_id] = {
        "title":title,
        "priority":priority,
        "done":done,
    }
    data["next_id"]+=1
    save_data(data)
    return task_id

def delete_task(task_id):
    data = load_data()
    if task_id not in data["tasks"]:
        return False
    del data["tasks"][task_id]
    save_data(data)
    return True

def update_task(task_id,**fields):
    data = load_data()
    if task_id not in data["tasks"]:
        return False
    data["tasks"][task_id].update(fields)
    save_data(data)
    return True

def toggle_done(task_id):
    data = load_data()
    if task_id not in data["tasks"]:
        return False
    task = data["tasks"][task_id]
    task["done"] = not task["done"] #simple toggle for the done
    save_data(data)
    return True

