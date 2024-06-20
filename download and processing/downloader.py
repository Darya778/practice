import time
from datetime import datetime, timedelta
import schedule
import sys
import requests
import zipfile

save_path = "/home/dasha/wotiwan/archive"

def unpack_archive(filepath):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(save_path)

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


schedule.every(1).day.at("15:30").do(download)

while True:
    schedule.run_pending()
    time.sleep(1)
