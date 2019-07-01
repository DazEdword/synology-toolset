from freezegun import freeze_time
from unittest.mock import patch

from synotools.common.utils import zip_folder


@freeze_time("2019-06-28")
@patch("synotools.common.utils.zipfile")
@patch("synotools.common.utils.logger")
@patch(
    "synotools.common.utils.os.walk",
    return_value=[("project-root", [], ["file-one.txt", "file_two.txt"])],
)
def test_creates_and_returns_zipname_with_passed_base_and_timestamp(os_walk_mock, *_):
    actual = zip_folder("my-test-file", "my/test/path")

    assert actual == "my-test-file-2019-06-28T00:00:00.zip"


@freeze_time("2019-06-28")
@patch("synotools.common.utils.zipfile")
@patch("synotools.common.utils.logger")
@patch(
    "synotools.common.utils.os.walk",
    return_value=[("project-root", [], ["file-one.txt", "file_two.txt"])],
)
def test_gets_filepaths_from_os_walk(os_walk_mock, logger_mock, *_):
    zip_folder("my-test-file", "my/test/path")

    assert (
        logger_mock.info.call_args_list[1][0][0]
        == "Zipping files: ['project-root/file-one.txt', 'project-root/file_two.txt']"
    )


@freeze_time("2019-06-28")
@patch("synotools.common.utils.logger")
@patch("synotools.common.utils.zipfile")
@patch(
    "synotools.common.utils.os.walk",
    return_value=[("project-root", [], ["file-one.txt", "file-two.txt"])],
)
def test_zips_files_with_flattened_paths(os_walk_mock, zipfile_mock, *_):
    zip_folder("my-test-file", "my/test/path")

    zipfile_mock.ZipFile.assert_called_once_with(
        "my-test-file-2019-06-28T00:00:00.zip", "w"
    )

    zipfile_mock.ZipFile.return_value.call_count == 2
    assert (
        zipfile_mock.ZipFile.return_value.write.call_args_list[0][0][0]
        == "project-root/file-one.txt"
    )
    assert (
        zipfile_mock.ZipFile.return_value.write.call_args_list[0][0][1]
        == "file-one.txt"
    )
    assert (
        zipfile_mock.ZipFile.return_value.write.call_args_list[1][0][0]
        == "project-root/file-two.txt"
    )
    assert (
        zipfile_mock.ZipFile.return_value.write.call_args_list[1][0][1]
        == "file-two.txt"
    )


@freeze_time("2019-06-28")
@patch("synotools.common.utils.logger")
@patch("synotools.common.utils.zipfile")
@patch(
    "synotools.common.utils.os.walk",
    return_value=[("project-root", [], ["file-one.txt", "file-two.txt"])],
)
def test_adds_path_to_filename_when_destination_dir_is_provided(
    os_walk_mock, zipfile_mock, *_
):
    actual = zip_folder("my-test-file", "my/test/path", "my/destination/path")
    expected = "my/destination/path/my-test-file-2019-06-28T00:00:00.zip"

    assert actual == expected
