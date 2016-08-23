import datetime
import os
import re
import time

import exifread

ext_list = [".jpg", ".jpeg", ".mov", ".mts", ".mp4"]


def read_dir(path):
    files = []
    if path != "":
        lst = os.listdir(path)
        lst.sort()
        for file in lst:
            if os.path.splitext(file)[1].lower() in ext_list:
                files.append(
                    (os.path.splitext(file), rename(os.path.join(path, file))))
    return files


def get_older_date_from_file(file_path):
    date = os.path.getmtime(file_path) if os.path.getmtime(file_path) < os.path.getctime(
        file_path) else os.path.getctime(
        file_path)

    # check Android file names
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    try:
        date_from_filename = time.mktime(time.strptime(str(file_name), "%Y%m%d_%H%M%S"))
    except ValueError:
        print(file_name)
        return date

    date = date_from_filename if date_from_filename is not None and date > date_from_filename else date
    return date


def rename(file):
    existing_files_pattern = re.compile("\\d+-\\d+-\\d+_\\d+\\.\\d+\\.\\d+(_\\d+)?")
    if existing_files_pattern.match(str(os.path.basename(file))) is not None:
        return "Keine Änderung"

    with open(file, 'rb') as f:
        tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
        date = tags.get('EXIF DateTimeOriginal')

    if date is None:
        date = get_older_date_from_file(file)
    else:
        # print(date)
        date = time.mktime(time.strptime(str(date), "%Y:%m:%d %H:%M:%S"))

    file_formatted_datetime = (datetime.datetime.fromtimestamp(date)).strftime("%Y-%m-%d_%H.%M.%S")

    file_ext = os.path.splitext(file)[1].lower()

    file_path = os.path.dirname(file)

    new_filename = os.path.join(file_path, file_formatted_datetime)

    return file_formatted_datetime

    # i = ""
    # while os.path.exists(new_filename + i + file_ext):
    #     i = "_01" if i == "" else "_" + "{:0>2d}".format(int(i.strip("_")) + 1)

    # os.rename(file, new_filename + i + file_ext)
