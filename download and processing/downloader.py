import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '../log'))
import time
from datetime import datetime, timedelta
import schedule
import sys
import requests
import zipfile
import os
import subprocess
import gzip
import shutil

abs_path = "/home/dasha/wotiwan/"
save_path = "/home/dasha/wotiwan/archive"
sites_list = []

def download():
    date = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"{abs_path}{date}.zip"
    headers = {}
    if os.path.exists(file_name):
        current_size = os.path.getsize(file_name)
        headers['Range'] = f'bytes={current_size}-'
    else:
        current_size = 0
    total_length=0
    with open(file_name, "ab") as f:
        print("Скачивание %s" % file_name)
        log_message("info", "200 OK Скачивание %s" % file_name)
        try:
            response = requests.get(link, headers=headers, stream=True)
            response.raise_for_status()

            if response.status_code == 416:
                print("Файл уже полностью загружен.")
                log_message("info", "200 OK Файл %s загружен." % file_name)
                return file_name

            total_length = response.headers.get('content-length')
            if total_length is not None:
                total_length = int(total_length) + current_size

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = current_size
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке: {e}")
            log_message("error", f"Ошибка при загрузке: {e}")
            return None
            
    if os.path.getsize(file_name) == total_length:
        print("Файл загружен полностью.")
        return file_name
    else:
        print("Файл не загружен полностью, повторная попытка.")
        return None

def download_until_complete():
    while True:
        path = download()
        if path:
            return path
        print("Повторная попытка загрузки...")
        time.sleep(10)  # Wait a bit before retrying

def unpack_archive(filepath):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(save_path)
        log_message("info", "200 OK Архив распакован.")


def decompress_gz_files():
    for root, dirs, files in os.walk(save_path):
        for file in files:
            if file.endswith('.gz'):
                file_path = os.path.join(root, file)
                with gzip.open(file_path, 'rb') as f_in:
                    with open(file_path[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                        log_message("info", "200 OK Файлы gz распакованы.")
                os.remove(file_path)


def decompress_Z_files():
    for root, dirs, files in os.walk(save_path):
        for file in files:
            if file.endswith('.Z'):
                file_path = os.path.join(root, file)
                subprocess.run(['/usr/bin/uncompress', file_path])
                log_message("info", "200 OK Файлы Z распакованы.")


def convert_files():
    for root, dirs, files in os.walk(save_path):
        for file in files:
            if file.endswith('.crx') or file.endswith('.24d'):
                file_path = os.path.join(root, file)
                subprocess.run(['/home/dasha/wotiwan/CRX2RNX', file_path])
                os.remove(file_path)
                print("done!")
                log_message("info", "200 OK Файлы конвертированы в форматы rnx и 24o.")

def create_directory_structure():
    date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    year = date.split('-')[0]
    day_of_year = datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
    target_dir = os.path.join(save_path, year, f'{day_of_year:03d}')

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        log_message("info", "200 OK Создана папка %s" % target_dir)

    for root, dirs, files in os.walk(save_path):
        print(dirs)
        for file in files:
            if root == save_path:
                if file.endswith('.rnx') or file.endswith('.24o'):
                    if file.endswith('.rnx'):
                        site_name = file.split('_')[0]
                        sites_list.append(site_name)
                    else:
                        site_name = file.split('.')[0]
                        sites_list.append(site_name)
                    site_dir = os.path.join(target_dir, site_name)
                    if not os.path.exists(site_dir):
                        os.makedirs(site_dir)
                    shutil.move(os.path.join(root, file), os.path.join(site_dir, file))
        log_message("info", "200 OK Все файлы распределены по папкам.")


def get_first_level_directories(time_dif):
    try:
        date = (datetime.now() - timedelta(days=6-time_dif)).strftime('%Y-%m-%d')
        day_of_year = datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
        directory_path = f"/home/dasha/wotiwan/archive/2024/{day_of_year}"
        entries = os.listdir(directory_path)
        directories = [entry for entry in entries if os.path.isdir(os.path.join(directory_pa>
        return directories
    except Exception as e:
        print(f"Ошибка: {e}")
        log_message("error", "Ошибка: {e}")
        return []

                                                                                
def main():
    path = download_until_complete()
    unpack_archive(path)
    decompress_gz_files()
    decompress_Z_files()
    convert_files()
    create_directory_structure()
    directories = get_first_level_directories(1)
    for i in sites_list:
        daemons_list.write(i + '\n')
    print("Done! Going to sleep.")

        
def ensure_download_complete():
    date = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    file_name = f"{abs_path}{date}.zip"
    if os.path.exists(file_name):
        current_size = os.path.getsize(file_name)
        link = f"https://api.simurg.space/datafiles/map_files?date={date}"
        try:
            response = requests.head(link)
            response.raise_for_status()
            total_length = response.headers.get('content-length')
            if total_length is not None:
                total_length = int(total_length)
                if current_size >= total_length:
                    print("Файл загружен полностью.")
                    return True
                else:
                    print(f"Файл не загружен полностью: {current_size}/{total_length}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при проверке: {e}")
    else:
        print("Файл не существует.")
    return False

def run_scheduled_task():
    if ensure_download_complete():
        main()
    else:
        print("Загрузка не завершена, повторная попытка.")
        download_until_complete()
        main()

schedule.every(1).day.at("18:00").do(run_scheduled_task)

while True:
    schedule.run_pending()
    if not ensure_download_complete():
        print("Загрузка не завершена, повторная попытка.")
        download_until_complete()
    time.sleep(1)

