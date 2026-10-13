from core.storage import load_sessions
from screens.TimerScreen import PHASE_DURATIONS
from datetime import datetime,date,timedelta

def filter_sessions(since,until): # will be used later this well filter sessions out, refactor the rest of the functions that use it
    sessions = load_sessions()
    results  = []
    for session in sessions:

        if not session["completed"]:
            continue
        if session["phase"] != "work":
            continue
        session_date = datetime.fromisoformat(session["start"])
        if not since <= session_date <= until:
            continue
        results.append(session)

    return results


def current_streak() -> int:
    sessions = load_sessions()
    dates = []
    for session in sessions:
        if session["completed"] == True and session["phase"] == "work":
            dt = datetime.fromisoformat(session["start"]).date()
            dates.append(dt)
    if len(dates) == 0:
        return 0
    today = datetime.today().date()
    if today in dates:
        cursor = today
    elif (today - timedelta(days = 1)) in dates:
        cursor = today - timedelta(days=1)
    else:
        return 0

    streak = 0
    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak 


def total_focus_time(since,until) -> float:
    since = date.fromisoformat(since) if isinstance(since, str) else since
    until = date.fromisoformat(until) if isinstance(until, str) else until
    
    sessions = load_sessions()
    
    total = 0

    for session in sessions:
        session_date = datetime.fromisoformat(session["start"]).date()

        if since<= session_date <= until:
            if session["completed"] == True and session["phase"] == "work":

                    start_dt = datetime.fromisoformat(session["start"])

                    end_dt = datetime.fromisoformat(session["end"])

                    duration = end_dt - start_dt

                    secounds = int(duration.total_seconds())
                    minutes = secounds // 60
                    total += secounds
    return total

def completed_work_sessions():
    sessions = load_sessions()
    completed = []
    for session in sessions:
        if session["completed"] == True and session["phase"] == "work":
            completed.append(session)

    return completed


def sessions_per_day(sessions, days=180):
    result = {}
    for session in completed_work_sessions():
        start_dt = datetime.fromisoformat(session["start"]).date()

        result[start_dt] = result.get(start_dt,0) + 1

    return result

def longest_streak(sessions):
    pass
