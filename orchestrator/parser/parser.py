import sys
import os
current_dir = os.path.dirname(os.path.abspath(file))
sys.path.insert(1, os.path.join(current_dir, '../../log'))
import time
from datetime import datetime, timedelta
import schedule
import os


def get_first_level_directories(time_dif):
    try:
        date = (datetime.now() - timedelta(days=6-time_dif)).strftime('%Y-%m-%d')
        day_of_year = datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
        directory_path = f"/home/dasha/wotiwan/archive/2024/{day_of_year}"
        entries = os.listdir(directory_path)

        directories = [entry for entry in entries if os.path.isdir(os.path.join(directory_path, entry))]

        log_message("info", "200 OK Get directories.")
        return directories
    except Exception as e:
        log_message("error", f"Error: {e}")
        print(f"Error: {e}")
        return []


def write_directories_to_file(directories):
    try:
        file_path = "/home/dasha/wotiwan/orchestrator/daemons_to_load.txt"
        with open(file_path, 'w') as file:
            for directory in directories:
                file.write(directory + '\n')
    except Exception as e:
        log_message("error", f"Error writing to file: {e}")
        print(f"Error writing to file: {e}")


def main():
    directories = get_first_level_directories(1)
    write_directories_to_file(directories)
    print("Done! Going to sleep.")


directories = get_first_level_directories(0)
write_directories_to_file(directories)


schedule.every(1).day.at("23:25").do(main)


while True:
    schedule.run_pending()
    time.sleep(1)
