#!/usr/bin/env python

from click.testing import CliRunner
from group_closely_created_files.cli import cli
from pathlib import Path
import mock
import os

def test_cli_with_default_options():
    runner = CliRunner()

    with runner.isolated_filesystem() as td:
        src_directory = (Path(td) / 'src')
        src_directory.mkdir()
        dst_directory = Path(td) / 'dst'

        timestamps = [
            50,
            200, 210,
            400, 410, 530,
            651
        ]

        test_files = [(src_directory / str(timestamp)) for timestamp in timestamps]
        [test_file.touch() for test_file in test_files]
        [os.utime(test_file.resolve(), (int(test_file.name), int(test_file.name))) for test_file in test_files]

        result = runner.invoke(cli, [str(src_directory), str(dst_directory)])
        assert result.exit_code == 0
        assert result.output == ''
        copied_directories = list(dst_directory.glob('*'))
        copied_items = list(dst_directory.glob('**/*'))

        assert len([item for item in copied_items if item.is_file()]) == 7
        assert len(copied_directories) == 4

        assert '1970-01-01_00:03:20:::2' in str(copied_items[0])
        assert '1970-01-01_00:00:50:::1' in str(copied_items[1])
        assert '1970-01-01_00:06:40:::3' in str(copied_items[2])
        assert '1970-01-01_00:10:51:::1' in str(copied_items[3])
        assert '1970-01-01_00:03:20:::2/210' in str(copied_items[4])
        assert '1970-01-01_00:03:20:::2/200' in str(copied_items[5])
        assert '1970-01-01_00:00:50:::1/50' in str(copied_items[6])
        assert '1970-01-01_00:06:40:::3/410' in str(copied_items[7])
        assert '1970-01-01_00:06:40:::3/530' in str(copied_items[8])
        assert '1970-01-01_00:06:40:::3/400' in str(copied_items[9])
        assert '1970-01-01_00:10:51:::1/651' in str(copied_items[10])

        # assert files are copied and has not been modified
        copied_source_files = [file for file in src_directory.glob('*') if int(file.stat().st_mtime) == int(file.name) ]
        assert len(copied_source_files) == 7

def test_cli_to_skip_non_files():
    runner = CliRunner()

    with runner.isolated_filesystem() as td:
        src_directory = (Path(td) / 'src')
        src_directory.mkdir()
        dst_directory = Path(td) / 'dst'

        timestamps = [
            50,
            200, 210,
            400,
            410,
            530,
            651
        ]
        is_file = [ False, True, True, True, False, True, True ]

        test_items = [(src_directory / str(timestamp)) for timestamp in timestamps]
        [test_item.touch() for (idx, test_item) in enumerate(test_items) if is_file[idx]]
        [test_item.mkdir() for (idx, test_item) in enumerate(test_items) if not is_file[idx]]
        [os.utime(test_item.resolve(), (int(test_item.name), int(test_item.name))) for test_item in test_items]

        result = runner.invoke(cli, [str(src_directory), str(dst_directory)])
        assert result.exit_code == 0
        assert result.output == ''
        copied_directories = (list(dst_directory.glob('*')))
        copied_items = list(dst_directory.glob('**/*'))
        assert len(copied_directories) == 4
        assert len([item for item in copied_items if item.is_file()]) == 5

        assert '1970-01-01_00:03:20:::2' in str(copied_items[0])
        assert '1970-01-01_00:08:50:::1' in str(copied_items[1])
        assert '1970-01-01_00:06:40:::1' in str(copied_items[2])
        assert '1970-01-01_00:10:51:::1' in str(copied_items[3])
        assert '1970-01-01_00:03:20:::2/210' in str(copied_items[4])
        assert '1970-01-01_00:03:20:::2/200' in str(copied_items[5])
        assert '1970-01-01_00:08:50:::1/530' in str(copied_items[6])
        assert '1970-01-01_00:06:40:::1/400' in str(copied_items[7])
        assert '1970-01-01_00:10:51:::1/651' in str(copied_items[8])

def test_cli_with_move_option():
    runner = CliRunner()

    with runner.isolated_filesystem() as td:
        src_directory = (Path(td) / 'src')
        src_directory.mkdir()
        dst_directory = Path(td) / 'dst'

        timestamps = [
            50,
            200, 210,
            400, 410, 530,
            651
        ]

        test_files = [(src_directory / str(timestamp)) for timestamp in timestamps]
        [test_file.touch() for test_file in test_files]
        [os.utime(test_file.resolve(), (int(test_file.name), int(test_file.name))) for test_file in test_files]

        result = runner.invoke(cli, [str(src_directory), str(dst_directory), '-m', 'move'])
        assert result.exit_code == 0
        assert result.output == ''
        moved_directories = (list(dst_directory.glob('*')))
        moved_items = list(dst_directory.glob('**/*'))
        assert len([item for item in moved_items if item.is_file()]) == 7
        assert len(moved_directories) == 4

        assert '1970-01-01_00:03:20:::2' in str(moved_items[0])
        assert '1970-01-01_00:00:50:::1' in str(moved_items[1])
        assert '1970-01-01_00:06:40:::3' in str(moved_items[2])
        assert '1970-01-01_00:10:51:::1' in str(moved_items[3])
        assert '1970-01-01_00:03:20:::2/210' in str(moved_items[4])
        assert '1970-01-01_00:03:20:::2/200' in str(moved_items[5])
        assert '1970-01-01_00:00:50:::1/50' in str(moved_items[6])
        assert '1970-01-01_00:06:40:::3/410' in str(moved_items[7])
        assert '1970-01-01_00:06:40:::3/530' in str(moved_items[8])
        assert '1970-01-01_00:06:40:::3/400' in str(moved_items[9])
        assert '1970-01-01_00:10:51:::1/651' in str(moved_items[10])

        # assert files are moved and no more
        copied_source_files = [file for file in src_directory.glob('*') if int(file.stat().st_mtime) == int(file.name) ]
        assert len(copied_source_files) == 0

def test_cli_with_distance_option():
    runner = CliRunner()

    with runner.isolated_filesystem() as td:
        src_directory = (Path(td) / 'src')
        src_directory.mkdir()
        dst_directory = Path(td) / 'dst'

        timestamps = [
            50, 200, 210,
            400, 410, 530, 651
        ]

        test_files = [(src_directory / str(timestamp)) for timestamp in timestamps]
        [test_file.touch() for test_file in test_files]
        [os.utime(test_file.resolve(), (int(test_file.name), int(test_file.name))) for test_file in test_files]

        result = runner.invoke(cli, [str(src_directory), str(dst_directory), '-d', '150'])
        assert result.exit_code == 0
        assert result.output == ''
        copied_directories = (list(dst_directory.glob('*')))

        assert len([item for item in dst_directory.glob('**/*') if item.is_file()]) == 7
        assert len(copied_directories) == 2
        assert "1970-01-01_00:00:50:::3" in str(copied_directories[0])
        assert "1970-01-01_00:06:40:::4" in str(copied_directories[1])

        # assert files are copied and not modified
        copied_source_files = [file for file in src_directory.glob('*') if int(file.stat().st_mtime) == int(file.name) ]
        assert len(copied_source_files) == 7

def test_cli_with_min_group_size_option():
    runner = CliRunner()

    with runner.isolated_filesystem() as td:
        src_directory = (Path(td) / 'src')
        src_directory.mkdir()
        dst_directory = Path(td) / 'dst'

        timestamps = [
            50,
            200, 210,
            400, 410, 530,
            651
        ]

        test_files = [(src_directory / str(timestamp)) for timestamp in timestamps]
        [test_file.touch() for test_file in test_files]
        [os.utime(test_file.resolve(), (int(test_file.name), int(test_file.name))) for test_file in test_files]

        result = runner.invoke(cli, [str(src_directory), str(dst_directory), '-n', 2])
        assert result.exit_code == 0
        assert result.output == ''
        copied_directories = list(dst_directory.glob('*'))
        copied_items = list(dst_directory.glob('**/*'))

        assert len([item for item in copied_items if item.is_file()]) == 5
        assert len(copied_directories) == 2

        assert '1970-01-01_00:03:20:::2' in str(copied_items[0])
        assert '1970-01-01_00:06:40:::3' in str(copied_items[1])
        assert '1970-01-01_00:03:20:::2/210' in str(copied_items[2])
        assert '1970-01-01_00:03:20:::2/200' in str(copied_items[3])
        assert '1970-01-01_00:06:40:::3/410' in str(copied_items[4])
        assert '1970-01-01_00:06:40:::3/530' in str(copied_items[5])
        assert '1970-01-01_00:06:40:::3/400' in str(copied_items[6])

        # assert files are copied and has not been modified
        copied_source_files = [file for file in src_directory.glob('*') if int(file.stat().st_mtime) == int(file.name) ]
        assert len(copied_source_files) == 7