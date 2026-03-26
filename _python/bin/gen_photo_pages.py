"""
generate photo pages
"""

import click
from click import command, argument
import json
from typing import Any

from photo_pages.photo_page_collection import PhotoPageCollection


@command(help="Reduce sizes of JPEG files")
@argument(
    "config_file", type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True)
)
def main(config_file: str) -> None:
    with open(config_file) as fid:
        photo_page_data: dict[str, Any] = json.load(fid)

    photo_page_collection: PhotoPageCollection = PhotoPageCollection()

    for photo_page in photo_page_data["photo_directories"]:
        for idx in range(1, len(photo_page)):
            photo_page_collection.insert_child_page(photo_page[:idx], photo_page[idx])
        photo_page_collection.create_a_photo_page(photo_page)

    photo_page_collection.write_photo_pages(
        photo_page_data["write_directory"], photo_page_data["photo_directory"]
    )


if __name__ == "__main__":
    main()
