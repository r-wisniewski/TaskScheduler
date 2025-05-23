from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import logging, scheduler, uvicorn, executor
from typing import Optional
import threading, sqlite3
from datetime import datetime

# initialize FastAPI and Jinja2 instances
app = FastAPI()
templates = Jinja2Templates(directory="HTMLfiles")

logging.basicConfig(level=logging.INFO) #set up logging

@app.get("/")
def root(request: Request):
    tasks = scheduler.get_scheduled_tasks()  # Get the scheduled tasks from the scheduler
    return templates.TemplateResponse("index.html", 
                                      {"request": request, "task_table": tasks}) # render index.html

@app.post("/schedule")
async def schedule(
    request: Request,
    trigger_type: str = Form(...), # Gets value from name="trigger_type"
    run_date: Optional[str] = Form(None), # Gets value from name="run_date"
    interval_seconds: Optional[str] = Form(None), # Gets value from name="interval_seconds"
    cron_hour: Optional[str] = Form(None), # Gets value from name="cron_hour"
    cron_minute: Optional[str] = Form(None), # Gets value from name="cron_minute"
    cron_second: Optional[str] = Form(None), # Gets value from name="cron_second"
    command: str = Form(...), # Gets value from name="command"
):
    try:
        trigger_kwargs = {}
        error_msg = None
        if trigger_type == 'date':
            trigger_kwargs['trigger_type'] = trigger_type
            if not run_date:
                raise ValueError("Run date cannot be empty for date trigger")
            # strptime() will raise an error if the date format is incorrect
            trigger_kwargs['run_date'] = datetime.strptime(run_date, "%Y-%m-%dT%H:%M:%S")
            trigger_kwargs['interval_seconds'] =  None
            trigger_kwargs['cron_hour'] = None
            trigger_kwargs['cron_minute'] = None
            trigger_kwargs['cron_second'] = None
            trigger_kwargs['last_run'] = None
            if not command:
                raise ValueError("Command cannot be empty for date trigger")
            trigger_kwargs['command'] = command # Command to run
        elif trigger_type == 'interval':
            trigger_kwargs['trigger_type'] = trigger_type
            trigger_kwargs['run_date'] = None
            trigger_kwargs['interval_seconds'] = int(interval_seconds) # Run every interval seconds from now
            trigger_kwargs['cron_hour'] = None
            trigger_kwargs['cron_minute'] = None
            trigger_kwargs['cron_second'] = None
            trigger_kwargs['last_run'] = None
            if not command:
                raise ValueError("Command cannot be empty for date trigger")
            trigger_kwargs['command'] = command # Command to run
        elif trigger_type == 'cron':
            trigger_kwargs['trigger_type'] = trigger_type
            trigger_kwargs['run_date'] = None
            trigger_kwargs['interval_seconds'] = None
            #check for empty values and values of out range
            if not cron_hour or not cron_minute or not cron_second:
                raise ValueError("Cron hour, minute, and second cannot be empty for cron trigger")
            if int(cron_hour) < 0 or int(cron_hour) > 23:
                raise ValueError("Cron hour must be between 0 and 23")
            if int(cron_minute) < 0 or int(cron_minute) > 59:
                raise ValueError("Cron minute must be between 0 and 59")
            if int(cron_second) < 0 or int(cron_second) > 59:
                raise ValueError("Cron second must be between 0 and 59")
            trigger_kwargs['cron_hour'] = int(cron_hour)
            trigger_kwargs['cron_minute'] = int(cron_minute)
            trigger_kwargs['cron_second'] = int(cron_second)
            trigger_kwargs['last_run'] = None
            if not command:
                raise ValueError("Command cannot be empty for date trigger")
            trigger_kwargs['command'] = command # Command to run

        scheduler.schedule_task(**trigger_kwargs) #schedule task
        return RedirectResponse("/", status_code=303) #redirect back to root page
    
    except Exception as e:
        # type error found, return error message and load index.html w/ error
        error_msg = str(e)
        tasks = scheduler.get_scheduled_tasks()
        return templates.TemplateResponse("index.html", {"request": request, "task_table": tasks, "error_msg": error_msg})

if __name__ == "__main__":
    # connect to SQLite DB and create the task table if it doesn't exist
    with sqlite3.connect('task_db.db') as connection:
        cursor = connection.cursor()
        #check if the task table exists. If not, create it
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS task_table (
                command TEXT,
                trigger_type TEXT,
                run_date TEXT,
                interval_seconds INT,
                last_run TEXT,
                cron_hour INT,
                cron_minute INT,
                cron_second INT
            );
            '''
        cursor.execute(create_table_query)
        connection.commit()

    #make threads for executor and uvicorn server
    threads = []
    # 1 Thread for executor
    t_executor = threading.Thread(target=executor.run_executor)
    threads.append(t_executor)
    t_executor.start()

    # 1 Thread for uvicorn server
    t_uvicorn = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "127.0.0.1", "port": 8000})
    threads.append(t_uvicorn)
    t_uvicorn.start()

    # Wait for both threads to finish
    for t in threads:
        t.join()