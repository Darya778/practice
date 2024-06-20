import time
from datetime import datetime, timedelta
import schedule
import sys
import requests
import zipfile
import subprocess
import gzip
import shutil


def download():   
    date = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"{date}.zip"
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')
    
        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()
    return file_name


save_path = "/home/dasha/wotiwan/archive"

def unpack_archive(filepath):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(save_path)


def decompress_gz_files():
    for root, dirs, files in os.walk(save_path):
        for file in files:
            if file.endswith('.gz'):
                file_path = os.path.join(root, file)
                with gzip.open(file_path, 'rb') as f_in:
                    with open(file_path[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(file_path)


def decompress_Z_files():
    for root, dirs, files in os.walk(save_path):
        for file in files:
            if file.endswith('.Z'):
                file_path = os.path.join(root, file)
                subprocess.run(['uncompress', file_path])

def convert_files():
    for root, dirs, files in os.walk(save_path):
        for file in files:
            if file.endswith('.crx') or file.endswith('.24d'):
                file_path = os.path.join(root, file)
                subprocess.run(['/home/dasha/wotiwan/CRX2RNX', file_path])
                os.remove(file_path)
                print("done!")


def create_directory_structure():
    date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    year = date.split('-')[0]
    day_of_year = datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
    target_dir = os.path.join(save_path, year, f'{day_of_year:03d}')

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(save_path):
        print(dirs)
        for file in files:
            if root == save_path:
                if file.endswith('.rnx') or file.endswith('.24o'):
                    if file.endswith('.rnx'):
                        site_name = file.split('_')[0]
                    else:
                        site_name = file.split('.')[0]
                    site_dir = os.path.join(target_dir, site_name)
                    if not os.path.exists(site_dir):
                        os.makedirs(site_dir)
                    shutil.move(os.path.join(root, file), os.path.join(site_dir, file))


def main():
    path = download()
    unpack_archive(path)
    decompress_gz_files()
    decompress_Z_files()
    convert_files()
    create_directory_structure()
    print("Done! Going to sleep.")


schedule.every(1).day.at("14:30").do(download)

while True:
    schedule.run_pending()
    time.sleep(1)
