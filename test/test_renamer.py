import os

from media_renamer.logic.renamer import generate_new_file_name


def test_generate_new_file_name():
    actual = generate_new_file_name(
        file_path=os.path.join(os.path.dirname(__file__), "data/DSCF2053.RAF"), ignore_already_renamed=False
    )
    assert actual == "2021-12-12_17-28-55.raf"
