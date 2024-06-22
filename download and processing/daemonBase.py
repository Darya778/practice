from gnss_tec import rnx
from datetime import datetime, timedelta
import time
import copy

receiver_name = "PENC00HUN"
lib_path = "/home/dasha/wotiwan/archive"
data_dict = {}
data_dict_old = {}


def get_dict(time_dif):
    data_dict.clear()
    date = (datetime.now() - timedelta(days=6-time_dif)).strftime('%Y-%m-%d')
    year = date.split('-')[0]
    day_of_year = datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
    target_dir = f'/{lib_path}/{year}/{day_of_year:03d}/{receiver_name}'

    file_name = f'/{receiver_name}_R_{year}{day_of_year:03d}0000_01D_30S_MO.rnx'

    with open(f'{target_dir}{file_name}') as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            time_key = str(tec.timestamp).split(' ')[1]
            tec_info = '{} {}: {} {}'.format(
                tec.timestamp,
                tec.satellite,
                tec.phase_tec,
                tec.p_range_tec,
            )
            if time_key not in data_dict:
                data_dict[time_key] = []
            data_dict[time_key].append(tec_info)


get_dict(0)
new_dict_ready = False

while True:
    date_now = str(datetime.now().strftime('%H:%M:%S'))
    if date_now >= "23:00:00" and not new_dict_ready:
        data_dict_old.clear()
        data_dict_old = copy.deepcopy(data_dict)
        get_dict(1)
        new_dict_ready = True
    if date_now in data_dict and date_now < "23:00:00":
        new_dict_ready = False
        for key, value in data_dict.items():
            if key == date_now:
                print(value)
    elif date_now in data_dict_old and date_now >= "23:00:00":
        for key, value in data_dict_old.items():
            if key == date_now:
                print(value)
    time.sleep(1)
