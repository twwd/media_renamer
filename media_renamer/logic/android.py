import re
from datetime import datetime

from media_renamer.logic.time import utc_to_local


def check_whatsapp(file_name: str):
    if "-WA" in file_name:
        try:
            return datetime.strptime(str(file_name[4:12]), "%Y%m%d")
        except ValueError:
            pass
    return None


def check_signal(file_name: str):
    if "signal-" in file_name:
        try:
            return datetime.strptime(str(file_name[7:]), "%Y-%m-%d-%H%M%S")
        except ValueError:
            pass
    return None


def get_date_from_android_filename(file_name: str):
    d = None

    datetime_pattern_android = re.compile(r".*(20\d{2}\d{2}\d{2}_\d{2}\d{2}\d{2}).*")

    matches = datetime_pattern_android.match(file_name)

    if matches is not None:
        d = datetime.strptime(matches.group(1), "%Y%m%d_%H%M%S")
        # Pixel device use UTC time as filename
        if d is not None and file_name.startswith("PXL"):
            d = utc_to_local(d)

    if d is None:
        d = check_whatsapp(file_name)

    if d is None:
        d = check_signal(file_name)

    return d
