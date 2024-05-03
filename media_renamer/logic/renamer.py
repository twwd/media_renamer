# -*- coding: utf-8 -*-

import os
import re
import tempfile
from datetime import datetime

import exifread
import rawpy
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from media_renamer.logic.android import get_date_from_android_filename
from media_renamer.logic.time import utc_to_local

ext_list = [".jpg", ".jpeg", ".mov", ".mts", ".mp4", ".avi", ".raf"]


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
                self.file_names.append([os.path.basename(file), ""])

    def generate_new_file_names(self, ignore_already_renamed: bool = True, use_filesystem_timestamps: bool = False):
        self.update()
        for item in self.file_names:
            item[1] = generate_new_file_name(
                os.path.join(self.path, item[0]), ignore_already_renamed, use_filesystem_timestamps
            )

    def rename(self):
        for item in self.file_names:
            old_file_path = os.path.join(self.path, item[0])
            new_file_path = os.path.join(self.path, item[1])

            if old_file_path == new_file_path or item[1] == "":
                continue

            # Prevent duplicate file names
            new_file_ext = os.path.splitext(new_file_path)[1]
            new_file_path = os.path.splitext(new_file_path)[0]

            i = ""
            while os.path.exists(new_file_path + i + new_file_ext):
                i = "_01" if i == "" else "_" + "{:0>2d}".format(int(i.strip("_")) + 1)

            try:
                os.rename(old_file_path, f"{new_file_path}{i}{new_file_ext}")
            except FileNotFoundError:
                pass


def get_older_date_from_file(file_path):
    return datetime.fromtimestamp(
        os.path.getmtime(file_path)
        if os.path.getmtime(file_path) < os.path.getctime(file_path)
        else os.path.getctime(file_path)
    )


def get_date_from_hachoir(file_path):
    parser = createParser(file_path)
    if not parser:
        return None

    with parser:
        metadata = extractMetadata(parser)
    if not metadata:
        return None
    try:
        # For the tested files, it seems that the timestamp is saved in UTC, so we convert it to local time
        return utc_to_local(datetime.strptime(str(metadata.get("creation_date")), "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        return None


def get_date_from_exif(file_path):
    try:
        with open(file_path, "rb") as f:
            return _get_date_from_exif(f)
    except FileNotFoundError:
        return None


def _get_date_from_exif(f):
    tags = exifread.process_file(f, stop_tag="DateTimeOriginal")
    date = tags.get("EXIF DateTimeOriginal")
    # handle broken exif data
    fmt = "%Y:%m:%d %H:%M:%S"
    try:
        date = datetime.strptime(str(date), fmt)
    except ValueError as v:
        ulr = len(v.args[0].partition("unconverted data remains: ")[2])
        if ulr:
            date = datetime.strptime(str(date)[:-ulr], fmt)
        else:
            return None
    return date


def get_date_from_raf(file_path):
    try:
        with rawpy.imread(file_path) as raw:
            thumb = raw.extract_thumb()
        if thumb.format == rawpy.ThumbFormat.JPEG:
            # thumb.data is already in JPEG format, save as-is
            with tempfile.SpooledTemporaryFile(mode="wrb") as f:
                f.write(thumb.data)
                return _get_date_from_exif(f)

    except FileNotFoundError:
        return None


def generate_new_file_name(file_path: str, ignore_already_renamed: bool, use_filesystem_timestamps: bool) -> str:
    existing_files_pattern = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(_\d*)?(.*)")

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_ext = os.path.splitext(file_path)[1].lower()

    if ignore_already_renamed and existing_files_pattern.match(str(file_name)) is not None:
        return os.path.basename(file_path)

    date = get_date(file_name, file_ext, file_path, use_filesystem_timestamps)

    # if we did not find any date, use the original filename
    if date is None:
        return os.path.basename(file_path)

    file_formatted_datetime = date.strftime("%Y-%m-%d_%H-%M-%S")

    # Preserve Android moving and panorama pictures
    suffix = ""
    for preserved_suffix in [".MP", ".PANO", ".NIGHT", ".LS"]:
        if preserved_suffix in file_name:
            suffix += preserved_suffix

    # Handle old Android filenames for moving and panorama pictures
    prefix_map = {"MVIMG": ".MP", "PANO": ".PANO"}
    for prefix, mapped_suffix in prefix_map.items():
        if file_name.startswith(prefix):
            suffix += mapped_suffix

    return file_formatted_datetime + suffix + file_ext


def get_date(file_name: str, file_ext: str, file_path: str, use_filesystem_timestamps: bool) -> datetime | None:
    date = get_date_from_exif(file_path)
    if date is None and file_ext == ".raf":
        date = get_date_from_raf(file_path)
    if date is None:
        date = get_date_from_android_filename(file_name)
    if date is None:
        date = get_date_from_hachoir(file_path)
    if date is None and use_filesystem_timestamps:
        date = get_older_date_from_file(file_path)
    return date
