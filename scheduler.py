import logging, sqlite3
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

def delete_task(task_id):
    # connect to SQLite DB
    with sqlite3.connect('task_db.db') as connection:
        cursor = connection.cursor()
        # Build the delete query
        delete_query = f"DELETE FROM task_table WHERE id={task_id}"
        cursor.execute(delete_query)
        connection.commit()
        logging.info(f"Task with ID {task_id} deleted successfully")

def get_scheduled_tasks():
    tasks = []
    # connect to SQLite DB
    with sqlite3.connect('task_db.db') as connection:
        cursor = connection.cursor()
        query_str = "SELECT * FROM task_table"
        cursor.execute(query_str)
        rows = cursor.fetchall()
        for row in rows:
            task = {
                "id": row[0],
                "command": row[1],
                "trigger_type": row[2],
                "run_date": row[3],
                "interval_seconds": row[4],
                "last_run": row[5],
                "cron_hour": row[6],
                "cron_minute": row[7],
                "cron_second": row[8],
            }
            tasks.append(task)
    return tasks

def schedule_task(**trigger_kwargs):
    # connect to SQLite DB
    with sqlite3.connect('task_db.db') as connection:
        cursor = connection.cursor()
        # Build the insert query
        insert_query = '''
            INSERT OR IGNORE INTO task_table (
                command, trigger_type, run_date, interval_seconds, last_run, cron_hour, cron_minute, cron_second
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
        #dates are stored. Do not need to explicitly pass ID
        cursor.execute(insert_query, (
            trigger_kwargs['command'],
            trigger_kwargs['trigger_type'],
            trigger_kwargs['run_date'],
            trigger_kwargs['interval_seconds'],
            trigger_kwargs['last_run'],
            trigger_kwargs['cron_hour'],
            trigger_kwargs['cron_minute'],
            trigger_kwargs['cron_second']
        ))
        connection.commit()
        logging.info("Task scheduled successfully")