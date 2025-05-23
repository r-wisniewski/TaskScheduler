# TaskScheduler

A web-based task scheduler built with **FastAPI** and **Jinja2** that allows you to schedule, view, and delete tasks using different trigger types (date, interval, cron). Tasks are stored in a SQLite database and executed in the background.

## Features

- **Web UI**: Schedule tasks using a simple web interface.
- **Trigger Types**: Supports one-time (date), interval, and cron-style scheduling.
- **Task Management**: View all scheduled tasks and delete them as needed.
- **Persistent Storage**: Tasks are stored in a SQLite database.
- **Concurrent Execution**: Uses threading to run the web server and task executor simultaneously.
- **Error Handling**: User-friendly error messages for invalid input.

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/r-wisniewski/TaskScheduler.git
   cd TaskScheduler
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn jinja2 sqlite3
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Open your browser and go to:**
   ```
   http://127.0.0.1:8000/
   ```

## Usage

- **Schedule a Task:**  
  Fill out the form with the desired trigger type and command.  
  - **Date:** Runs once at the specified date/time.
  - **Interval:** Runs every N seconds.
  - **Cron:** Runs at a specific hour, minute, and second.

- **View Tasks:**  
  All scheduled tasks are listed in a table.

- **Delete a Task:**  
  Click the "Delete" button next to a task to remove it.

## Project Structure

```
TaskScheduler/
├── HTMLfiles/
│   └── index.html         # Jinja2 template for the web UI
├── main.py                # FastAPI app and entry point
├── scheduler.py           # Task scheduling logic (not shown)
├── executor.py            # Task execution logic (not shown)
├── task_db.db             # SQLite database (auto-created)
└── README.md
```

## Future Work

- **Add/Edit Task Logic:**  
  Extend `scheduler.py` and `executor.py` to support more complex scheduling or task types.
- **UI Improvements:**  
  Modify `HTMLfiles/index.html` for a better user experience.

##  Contact

Robin Wisniewski – [LinkedIn](https://www.linkedin.com/in/robin-wisniewski/) –  [wisniewski.ro@gmail.com](mailto:wisniewski.ro@gmail.com)

## License

[MIT](LICENSE)

---
