# -*- coding: utf-8 -*-

import datetime
import os
import re
import time

import exifread

ext_list = [".jpg", ".jpeg", ".mov", ".mts", ".mp4"]


class Directory:
    def __init__(self, path):
        if path == "" or not os.path.isdir(path):
            raise NotADirectoryError()
        self.path = path

        # list of lists with current and new file name
        self.file_names = []
        self.update()

    def update(self):
        self.file_names.clear()
        lst = os.listdir(self.path)
        lst.sort()
        for file in lst:
            if os.path.splitext(file)[1].lower() in ext_list:
                self.file_names.append(
                    [os.path.basename(file), ""])

    def generate_new_file_names(self):
        self.update()
        for item in self.file_names:
            item[1] = generate_new_file_name(os.path.join(self.path, item[0]))

    def rename(self):
        for item in self.file_names:
            old_file_path = os.path.join(self.path, item[0])
            new_file_path = os.path.join(self.path, item[1])

            if old_file_path == new_file_path:
                continue

            # Prevent duplicate file names
            new_file_ext = os.path.splitext(new_file_path)[1]
            new_file_path = os.path.splitext(new_file_path)[0]

            i = ""
            while os.path.exists(new_file_path + i + new_file_ext):
                i = "_01" if i == "" else "_" + "{:0>2d}".format(int(i.strip("_")) + 1)

            try:
                os.rename(old_file_path, new_file_path + i + new_file_ext)
            except FileNotFoundError:
                pass


def get_older_date_from_file(file_path):
    date = os.path.getmtime(file_path) if os.path.getmtime(file_path) < os.path.getctime(
        file_path) else os.path.getctime(
        file_path)

    # check Android file names
    file_name = os.path.splitext(os.path.basename(file_path))[0][0:14]
    try:
        date_from_filename = time.mktime(time.strptime(str(file_name), "%Y%m%d_%H%M%S"))
    except ValueError:
        return date

    date = date_from_filename if date_from_filename is not None and date > date_from_filename else date
    return date


def generate_new_file_name(file_path):
    existing_files_pattern = re.compile("\\d+-\\d+-\\d+_\\d+\\.\\d+\\.\\d+(_\\d+)?\..+")
    if existing_files_pattern.match(str(os.path.basename(file_path))) is not None:
        return os.path.basename(file_path)

    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
            date = tags.get('EXIF DateTimeOriginal')
    except FileNotFoundError:
        return None

    if date is None:
        date = get_older_date_from_file(file_path)
    else:
        fmt = "%Y:%m:%d %H:%M:%S"
        try:
            date = time.mktime(time.strptime(str(date), fmt))
        except ValueError as v:
            ulr = len(v.args[0].partition('unconverted data remains: ')[2])
            if ulr:
                date = time.mktime(time.strptime(str(date)[:-ulr], fmt))
            else:
                raise v

    file_formatted_datetime = (datetime.datetime.fromtimestamp(date)).strftime("%Y-%m-%d_%H.%M.%S")

    file_ext = os.path.splitext(file_path)[1].lower()

    return file_formatted_datetime + file_ext
