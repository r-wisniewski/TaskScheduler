import os, sqlite3
from time import sleep
from datetime import datetime

table_name = "task_table"

def run_executor():
    # connect to the SQLite database
    with sqlite3.connect('task_db.db') as connection:
        cursor = connection.cursor() #create the cursor object
        while True: #infinite loop to check for tasks
            sleep(2) #sleep for 2 second, then check for tasks
            query_str = f"SELECT * FROM {table_name}"
            cursor.execute(query_str)
            rows = cursor.fetchall()
            for row in rows: #row is a tuple
                # check the time and compare it to when the task should run
                now = datetime.now()
                if row[1] == "date":
                    # Execute the command if the date is less than or equal to now
                    if datetime.fromisoformat(row[2]) <= now:
                        command = row[0]
                        try:
                            os.system(command)
                            #remove task from DB
                            delete_str = f"DELETE FROM {table_name} WHERE command='{command}'"
                            cursor.execute(delete_str)
                            connection.commit()
                        except Exception as e:
                            print(f"Error executing command {command}: {e}")
                elif row[1] == "interval":
                    # Execute the command if the the command has not been run in the last interval seconds 
                    # if never run, then run
                    if row[4] is None:
                        command = row[0]
                        try:
                            os.system(command)
                            #set last run to now
                            update_str = f"UPDATE {table_name} SET last_run='{now}' WHERE command='{command}'"
                            cursor.execute(update_str)
                            connection.commit()
                        except Exception as e:
                            print(f"Error executing command {command}: {e}")
                    #check how long its been since the last run
                    else:
                        td = now - datetime.fromisoformat(row[4])
                        total_seconds_since_last_run = int(td.total_seconds())
                        if row[3] <= total_seconds_since_last_run:
                            command = row[0]
                            try:
                                os.system(command)
                                #set last run to now
                                update_str = f"UPDATE {table_name} SET last_run='{now}' WHERE command='{command}'"
                                cursor.execute(update_str)
                                connection.commit()
                            except Exception as e:
                                print(f"Error executing command {command}: {e}")
                elif row[1] == "cron":
                    #run daily at the minute, hour, second passed
                    # Extract hour, minute, and second
                    current_hour = now.hour
                    current_minute = now.minute
                    current_second = now.second
                    if (current_hour == row[5] and current_minute == row[6] and current_second == row[7]):
                        command = row[0]
                        try:
                            os.system(command)
                            #set last run to now
                            update_str = f"UPDATE {table_name} SET last_run='{now}' WHERE command='{command}'"
                            cursor.execute(update_str)
                            connection.commit()
                        except Exception as e:
                            print(f"Error executing command {command}: {e}")
                else:
                    print(f"Invalid trigger type: {row[1]}")
                    continue