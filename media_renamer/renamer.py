import datetime
import os
import re
import time

import exifread


def get_older_date_from_file(filename):
    date = os.path.getmtime(filename) if os.path.getmtime(filename) < os.path.getctime(
        filename) else os.path.getctime(
        filename)
    try:
        date_from_filename = time.mktime(time.strptime(str(date), "%Y%m%d_%H%M%S"))
    except ValueError:
        print("error")
        date_from_filename = None
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
