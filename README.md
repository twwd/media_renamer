# Media Renamer

Easily rename photos and videos according to the creation date.
It primarily considers the EXIF date.

## Installation

You need to have [poetry](https://python-poetry.org/) installed.

`poetry install`

## Launch

You can launch the GUI with:

`poetry run media_renamer`

## Example

`DSCF2053.RAF` → `2021-12-12_17-28-55.raf`

## Development

### Build with PyInstaller

Ensure that you have the poetry plugin for PyInstaller that comes with `poetry install` for Poetry 2.
Then, you can package the application with all of its dependencies into a single folder with `poetry build`.
