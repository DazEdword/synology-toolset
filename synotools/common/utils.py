import os
import zipfile
from datetime import datetime

from synotools.common.logging import get_logger

logger = get_logger(__name__)


def zip_folder(filename, origin_dir, destination_dir=None, exclude=[]):
    """Zips all files in a folder and returns path to zipped file"""
    logger.info(f"Preparing to zip all files in {origin_dir}...")
    file_paths = []

    # Not ISO, but Linux/Win compatible filename
    timestamp = datetime.utcnow().isoformat().replace(":", "")

    zipname = f"{filename}-{timestamp}.zip"

    if destination_dir:
        zipname = os.path.join(destination_dir, zipname)

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(origin_dir):
        for filename in files:
            _, file_ext = os.path.splitext(filename)
            if file_ext in exclude:
                continue

            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    logger.info(f"Zipping files: {file_paths}")

    # Writing files to a zipfile
    zip_file = zipfile.ZipFile(zipname, "w")
    with zip_file:
        for file in file_paths:
            flattened_file_path = os.path.basename(file)
            zip_file.write(file, flattened_file_path)

    logger.info(f"Files zipped in {zipname}")
    return zipname
