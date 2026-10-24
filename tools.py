import json
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).parent / 'assignments.json'

def load():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError('Database must contain a list')
    return data

def save(items):
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)

def valid_date(value):
    return date.fromisoformat(value)

def add_assignment(title, due_date, priority='medium', estimated_hours=2):
    if not isinstance(title, str) or not title.strip() or len(title) > 120:
        raise ValueError('Title must be 1–120 characters')
    valid_date(due_date)
    priority = priority.lower()
    if priority not in ('low', 'medium', 'high'):
        raise ValueError('Priority must be low, medium, or high')
    hours = float(estimated_hours)
    if not 0 < hours <= 100:
        raise ValueError('Estimated hours must be >0 and <=100')
    items = load()
    item = {'id': max((x['id'] for x in items), default=0)+1, 'title': title.strip(), 'due_date': due_date, 'priority': priority, 'estimated_hours': hours, 'status': 'pending'}
    items.append(item)
    save(items)
    return item

def list_assignments(status='all'):
    if status not in ('all','pending','completed'):
        raise ValueError('Invalid status')
    return sorted((x for x in load() if status == 'all' or x['status'] == status), key=lambda x:x['due_date'])

def check_deadlines(days=7):
    days = int(days)
    if not 0 <= days <= 365:
        raise ValueError('Days must be 0–365')
    today = date.today()
    return [{'days_remaining':(valid_date(x['due_date'])-today).days, **x} for x in list_assignments('pending') if valid_date(x['due_date']) <= today + timedelta(days=days)]

def update_status(assignment_id, status):
    if status not in ('pending','completed'):
        raise ValueError('Status must be pending or completed')
    items = load()
    for x in items:
        if x['id'] == int(assignment_id):
            x['status'] = status
            save(items)
            return x
    raise ValueError('Assignment ID not found')

def calculate_workload(days=7):
    tasks = check_deadlines(days)
    return {'days': int(days), 'assignment_count': len(tasks), 'total_estimated_hours': round(sum(x['estimated_hours'] for x in tasks),2), 'assignments': tasks}

def create_study_plan(days=7, daily_hours=2):
    days = int(days)
    daily_hours = float(daily_hours)
    if not 1 <= days <= 30 or not 0 < daily_hours <= 16:
        raise ValueError('Days must be 1–30 and daily hours >0 and <=16')
    today = date.today()
    tasks = sorted(list_assignments('pending'), key=lambda x:(x['due_date'], {'high':0,'medium':1,'low':2}[x['priority']]))
    remaining = {x['id']:x['estimated_hours'] for x in tasks}
    plan = []
    for offset in range(days):
        day = today + timedelta(days=offset)
        budget = daily_hours
        sessions = []
        for task in tasks:
            if budget <= 0: break
            if valid_date(task['due_date']) < day or remaining[task['id']] <= 0: continue
            hours = min(budget, remaining[task['id']])
            sessions.append({'assignment_id':task['id'], 'title':task['title'], 'hours':round(hours,2)})
            remaining[task['id']] -= hours
            budget -= hours
        plan.append({'date':day.isoformat(), 'sessions':sessions})
    return {'plan':plan, 'unscheduled_hours':{str(k):round(v,2) for k,v in remaining.items() if v > 0}, 'note':'Greedy earliest-deadline-first allocation; not a calendar booking.'}

TOOLS = {f.__name__: f for f in [add_assignment,list_assignments,check_deadlines,update_status,calculate_workload,create_study_plan]}
