"""
photo pages collection
"""

import os

from photo_pages.photo_page import PhotoPage


class PhotoPageCollection:
    def __init__(self) -> None:
        self.id_page_map: dict[tuple[str, ...], PhotoPage] = dict()

    def create_a_photo_page(self, dir_seq: list[str]) -> None:
        new_photo_page: PhotoPage = PhotoPage(dir_seq)
        assert new_photo_page.id_ not in self.id_page_map, (
            list(self.id_page_map.keys()),
            new_photo_page.id_,
            dir_seq,
        )
        new_photo_page.set_photo_directory(dir_seq)

        self.id_page_map[new_photo_page.id_] = new_photo_page

    def insert_child_page(self, parent_id: tuple[str, ...] | list[str], child_name: str) -> None:
        parent_id_: tuple[str, ...] = tuple(parent_id)

        if parent_id_ not in self.id_page_map:
            self.id_page_map[parent_id_] = PhotoPage(parent_id_)

        self.id_page_map[parent_id_].add_child(child_name)

    def write_photo_pages(self, directory: str, photo_root_dir: str) -> None:
        assert os.path.exists(directory), directory
        assert os.path.isdir(directory), directory

        master_page: PhotoPage = PhotoPage(tuple())

        for id_ in sorted(self.id_page_map.keys()):
            self.id_page_map[id_].write_page(directory, photo_root_dir)
            if len(id_) == 1:
                master_page.add_child(id_[0])

        master_page.write_page(directory)
