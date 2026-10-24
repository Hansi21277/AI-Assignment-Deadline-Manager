import json
import logging
import os
from ollama import Client
from tools import TOOLS

logging.basicConfig(filename='agent.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
MODEL = os.getenv('OLLAMA_MODEL','qwen2.5:3b')
SYSTEM = '''You are an academic assignment manager. Use tools for all task operations. Never claim a tool succeeded unless its result confirms success. For multi-step requests, continue calling tools until all steps are complete. Dates must be YYYY-MM-DD. Ask for missing essential details rather than inventing them. Keep responses concise. Today's date is provided in the user context. If tool returns an error, explain it and ask for correction.'''

def schemas():
    specs = {
        'add_assignment': ('Save a new assignment', {'title':{'type':'string'},'due_date':{'type':'string','description':'YYYY-MM-DD'},'priority':{'type':'string','enum':['low','medium','high']},'estimated_hours':{'type':'number'}}, ['title','due_date']),
        'list_assignments': ('List saved assignments', {'status':{'type':'string','enum':['all','pending','completed']}}, []),
        'check_deadlines': ('Find assignments due within N days including overdue', {'days':{'type':'integer'}}, []),
        'update_status': ('Mark an assignment completed or pending', {'assignment_id':{'type':'integer'},'status':{'type':'string','enum':['pending','completed']}}, ['assignment_id','status']),
        'calculate_workload': ('Calculate estimated workload due within N days', {'days':{'type':'integer'}}, []),
        'create_study_plan': ('Generate daily study sessions', {'days':{'type':'integer'},'daily_hours':{'type':'number'}}, []),
    }
    return [{'type':'function','function':{'name':name,'description':desc,'parameters':{'type':'object','properties':props,'required':required}}} for name,(desc,props,required) in specs.items()]

def run():
    from datetime import date
    client = Client(host=os.getenv('OLLAMA_HOST','http://localhost:11434'))
    messages = [{'role':'system','content':SYSTEM}]
    print('Assignment & Deadline Manager | type exit to quit')
    while True:
        try:
            question = input('\nYou: ').strip()
        except (KeyboardInterrupt,EOFError):
            break
        if question.lower() in ('exit','quit'): break
        if not question: continue
        messages.append({'role':'user','content':f'Today is {date.today().isoformat()}. {question}'})
        try:
            for step in range(10):
                response = client.chat(model=MODEL, messages=messages, tools=schemas())
                msg = response.message
                messages.append(msg.model_dump(exclude_none=True))
                calls = msg.tool_calls or []
                if not calls:
                    print('Agent:',msg.content or '(No response)')
                    break
                for call in calls:
                    name = call.function.name
                    args = call.function.arguments or {}
                    print(f'[TOOL CALL] {name}({json.dumps(args)})')
                    try:
                        if name not in TOOLS: raise ValueError('Unknown tool')
                        result = {'ok':True,'data':TOOLS[name](**args)}
                    except (ValueError,TypeError,KeyError,OSError,json.JSONDecodeError) as exc:
                        result = {'ok':False,'error':str(exc)}
                    print('[TOOL RESULT]',json.dumps(result,default=str))
                    logging.info('tool=%s args=%s result=%s',name,args,result)
                    messages.append({'role':'tool','tool_name':name,'content':json.dumps(result,default=str)})
            else:
                print('Agent: Tool limit reached; please simplify the request.')
        except Exception as exc:
            logging.exception('Agent request failed')
            print('Agent error:',str(exc),'\nCheck Ollama is running and model is downloaded.')

if __name__ == '__main__':
    run()
