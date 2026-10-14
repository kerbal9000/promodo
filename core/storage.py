import json,tempfile,os,copy
import datetime
from pathlib import Path

path_to_json = Path("storage/task.json")

DEFAULTS = {
    "tasks": {},
    "session_log": [],
    "next_task_id": 1,
    "next_session_id": 1,
    "next_id":1,
} # defualts for an mpty file


def load_tasks():
    
    return load_data()["tasks"]

def load_data() -> dict:
    if not path_to_json.exists():
        return copy.deepcopy(DEFAULTS)

    try:
        with open(path_to_json) as f:
            raw = f.read()
    except OSError:
        return copy.deepcopy(DEFAULTS)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return copy.deepcopy(DEFAULTS)

    if not isinstance(data, dict):
        return copy.deepcopy(DEFAULTS)

    data.setdefault("tasks", {})
    data.setdefault("session_log", [])
    data.setdefault("next_task_id", 1)
    data.setdefault("next_id", 1)
   
    if not isinstance(data["tasks"], dict):
        data["tasks"] = {}
    if not isinstance(data["session_log"], list):
        data["session_log"] = []

    return data

def save_data(data: dict) -> None: # saves data if file closes unexpectadly
    path_to_json.parent.mkdir(parents=True, exist_ok=True)
    tmp = path_to_json.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path_to_json)

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

def load_sessions() -> list[dict]: #history tab on mount will call it
    data = load_data()
    return data.get("session_log",{})

def log_session(start, end, phase, completed,task_id=None) -> int:
    data = load_data()
    
    if phase not in ("work", "short_break", "long_break"):
        raise ValueError(f"unknown phase: {phase}")

    if end < start:
        raise Exception("start is greater than end")

    if not isinstance(completed, bool):
        raise TypeError("completed must be bool")
    if not data["next_id"]:
        next_id = 0
    else:
        next_id = data["next_id"]
    
    #needs some defence against an empty file will bring up an errro
    data["session_log"].append({
        "id": next_id,
        "task_id": task_id,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "phase": phase,
        "completed": completed,
    })

    data["next_id"] += 1
    save_data(data)
    return next_id

def delete_session(session_id):
    data = load_data()
    if session_id not in data.get("session_log",{}):
        return False
    del data["session_log"][session_id]
    save_data(data)
    return True