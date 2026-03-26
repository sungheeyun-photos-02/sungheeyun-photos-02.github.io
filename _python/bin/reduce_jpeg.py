"""
Reduce sizes of all JPEG files in a given directory.
"""

import os
from logging import Logger, getLogger

import click
from click import command, argument, option

from freq_used.logging_utils import set_logging_basic_config

logger: Logger = getLogger()


@command(help="Reduce sizes of JPEG files")
@argument("directory", type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
@option("-q", "--quality", type=int, default=50, help="JPEG/MIFF/PNG compression level")
def main(directory: str, quality: int):

    assert quality > 0 and quality < 100, quality

    for filename in os.listdir(directory):
        root, ext = os.path.splitext(filename)
        if not (
            ext.lower() == ".jpg"
            or ext.lower() == ".jpeg"
            or ext.lower() == ".png"
            or ext.lower() == "miff"
        ):
            continue

        if root.endswith("-reduced"):
            continue

        trg_file_path: str = os.path.join(directory, root + f"-{quality}-reduced" + ext)
        if os.path.exists(trg_file_path):
            logger.warning(f"`{trg_file_path}' already exists... do nothing;")
        else:
            src_file_path: str = os.path.join(directory, filename)
            cmd: str = f'magick "{src_file_path}" -quality {quality} "{trg_file_path}"'
            logger.info(f"EXECUTING {cmd}")
            os.system(cmd)


if __name__ == "__main__":
    set_logging_basic_config(__file__)
    main()
