import os
import zipfile
import logging

from datetime import datetime


def zip_folder(filename, origin_dir, destination_dir=None):
    """Zips all files in a folder and returns path to zipped file"""

    file_paths = []

    timestamp = datetime.utcnow().isoformat()

    zipname = f"{filename}-{timestamp}.zip"

    if destination_dir:
        zipname = os.path.join(destination_dir, zipname)

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(origin_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    logging.info(f"Preparing to zip files: {file_paths}")

    # Writing files to a zipfile
    zip_file = zipfile.ZipFile(zipname, "w")
    with zip_file:
        for file in file_paths:
            flattened_file_path = os.path.basename(file)
            zip_file.write(file, flattened_file_path)

    return zipname
