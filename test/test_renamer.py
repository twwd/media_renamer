import shutil
from pathlib import Path

import pytest

from media_renamer.logic.renamer import Directory

TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    ("input_file_name", "expected_file_name"),
    (
        ("PXL_20241028_100532428.MP.jpg", "2024-10-28_11-05-32.MP.jpg"),
        ("2024-10-28_11-05-32_42.jpg", "2024-10-28_11-05-32_42.jpg"),
        ("schoenbrunn.jpg", "2024-10-28_10-59-32.jpg"),
        ("DSCF2053.RAF", "2021-12-12_17-28-55.raf"),
    ),
)
def test_rename(tmp_path: Path, input_file_name: str, expected_file_name: str):
    file_source_path = TEST_DATA_DIR / input_file_name
    file_target_path = tmp_path / input_file_name
    shutil.copy(file_source_path, file_target_path)

    directory = Directory(path=tmp_path)
    directory.generate_new_file_names()
    directory.rename()

    target_files = [f for f in tmp_path.iterdir()]
    assert len(target_files) == 1
    assert target_files[0].is_file()
    assert target_files[0].name == expected_file_name
