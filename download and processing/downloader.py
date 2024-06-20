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

def main():
    path = download()
    unpack_archive(path)
    decompress_gz_files()
    decompress_Z_files()
    convert_files()
    print("Done! Going to sleep.")

schedule.every(1).day.at("14:30").do(download)

while True:
    schedule.run_pending()
    time.sleep(1)
