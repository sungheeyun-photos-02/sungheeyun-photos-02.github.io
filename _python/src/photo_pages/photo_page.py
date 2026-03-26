"""
photo page
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo


class PhotoPage:

    def __init__(self, id_: tuple[str, ...] | list[str]) -> None:
        self.id_: tuple[str, ...] = tuple(id_)
        self.children: set[str] = set()
        self.photo_dir_seq: tuple[str, ...] | None = None

    def add_child(self, child: str) -> None:
        self.children.add(child)

    def set_photo_directory(self, dir_seq: list[str]) -> None:
        assert self.photo_dir_seq is None, self.photo_dir_seq
        self.photo_dir_seq = tuple(dir_seq)

    def write_page(self, directory: str, photo_root_dir: str | None = None) -> None:
        assert os.path.exists(directory), directory
        assert os.path.isdir(directory), directory

        assert photo_root_dir is None or os.path.exists(photo_root_dir), photo_root_dir
        assert photo_root_dir is None or os.path.isdir(photo_root_dir), photo_root_dir

        now_str: str = datetime.now(ZoneInfo("America/Los_Angeles")).strftime(
            "%a %b %d %H:%M:%S %Z %Y"
        )

        lines: list[str] = list()

        lines.append("---")
        lines.append("layout: single")
        lines.append(f"title: \"{os.path.join(*self.id_) if len(self.id_) > 0 else 'Photos'}\"")
        lines.append(f'permalink: "{self.permalink}"')
        lines.append("toc: false")
        lines.append('toc_label: "&nbsp;Table of Contents"')
        lines.append('toc_icon: "fa-solid fa-list"')
        lines.append("toc_sticky: true")
        lines.append(f"date: {now_str}")
        lines.append(f"last_modified_at: {now_str}")
        lines.append("---")

        if self.children:
            lines.append("")
            lines.append("<ul>")
            for child in sorted(self.children):
                lines.append("<li>")
                lines.append(f'\t<a href="{self.get_permalink(self.id_ + (child,))}">{child}</a>')
                lines.append("</li>")
            lines.append("</ul>")

        if self.photo_dir_seq is not None:
            assert photo_root_dir is not None
            photo_dir: str = os.path.join(photo_root_dir, *self.photo_dir_seq)
            assert os.path.exists(photo_dir), photo_dir
            assert os.path.isdir(photo_dir), photo_dir

            for filename in os.listdir(photo_dir):
                if filename == ".DS_Store":
                    continue
                if os.path.splitext(filename)[1].lower() == ".heic":
                    continue

                lines.append("")
                lines.append('<div class="img-container">')
                lines.append(
                    '\t<img style="max-width: 100%; max-height: none;" '
                    + f'src="/{os.path.join(photo_dir,filename)}">'
                )
                lines.append("</div>")

        with open(os.path.join(directory, self._file_name) + ".md", "w") as fid:
            fid.write("\n".join(lines) + "\n")

    @property
    def _file_name(self) -> str:
        return f"photo-page-{'-'.join(self.id_) if len(self.id_) > 0 else 'photo_master'}"

    @property
    def permalink(self) -> str:
        return self.get_permalink(self.id_)

    @staticmethod
    def get_permalink(id_: tuple[str, ...]) -> str:
        return "/" + ("/".join(id_) if len(id_) > 0 else "photo_master")
