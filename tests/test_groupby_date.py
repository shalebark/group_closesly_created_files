from pathlib import Path
from group_closely_created_files.groupby_date import read_dir, groupby_timestamp, as_transfer_list, transfer
from pytest import raises
import mock

def test_read_dir_can_read_directory(monkeypatch):
    monkeypatch.setattr(Path, 'resolve', lambda s: Path(s.name))
    monkeypatch.setattr(Path, 'stat', lambda s: type('', (object, ), dict(st_mtime=0.0)))
    monkeypatch.setattr(Path, 'is_file', lambda s: True)
    p0 = Path('0')

    monkeypatch.setattr(Path, 'glob', lambda s, pat: [p0])

    source = Path('/')
    output = read_dir(source)

    assert len(output) == 1
    assert output[0] == {'path': Path('0'), 'st_mtime': float(0)}

def test_read_dir_skips_directories(monkeypatch):
    monkeypatch.setattr(Path, 'resolve', lambda s: Path(s.name))
    monkeypatch.setattr(Path, 'stat', lambda s: type('', (object, ), dict(st_mtime=0.0)))
    monkeypatch.setattr(Path, 'is_file', lambda s: False)
    monkeypatch.setattr(Path, 'is_dir', lambda s: True)
    p0 = Path('0')

    monkeypatch.setattr(Path, 'glob', lambda s, pat: [p0])

    source = Path('/')
    output = read_dir(source)

    assert output == []

def test_groupby_timestamp_can_group_data(monkeypatch):
    timestamps = [0,1,2, 4, 5.1,5.9, 7,8,9, 11]
    data = list(map(lambda x: dict(path=str(x), st_mtime=float(x)), timestamps))
    grouped_data = groupby_timestamp(data, distance=1)

    assert len(grouped_data) == 5
    assert grouped_data[0] == [
        {'path': '0', 'st_mtime': 0.0},
        {'path': '1', 'st_mtime': 1.0},
        {'path': '2', 'st_mtime': 2.0},
    ]

    assert grouped_data[1] == [
        {'path': '4', 'st_mtime': 4.0},
    ]

    assert grouped_data[2] == [
        {'path': '5.1', 'st_mtime': 5.1},
        {'path': '5.9', 'st_mtime': 5.9},
    ]

    assert grouped_data[3] == [
        {'path': '7', 'st_mtime': 7.0},
        {'path': '8', 'st_mtime': 8.0},
        {'path': '9', 'st_mtime': 9.0},
    ]

    assert grouped_data[4] == [
        {'path': '11', 'st_mtime': 11.0}
    ]

def test_groupby_timestamp_can_group_randomized_data(monkeypatch):
    timestamps = [5.1, 0, 4, 7, 9, 5.9, 2, 8, 11, 1]
    data = list(map(lambda x: dict(path=str(x), st_mtime=float(x)), timestamps))
    grouped_data = groupby_timestamp(data, distance=1)

    assert len(grouped_data) == 5
    assert grouped_data[0] == [
        {'path': '0', 'st_mtime': 0.0},
        {'path': '1', 'st_mtime': 1.0},
        {'path': '2', 'st_mtime': 2.0},
    ]

    assert grouped_data[1] == [
        {'path': '4', 'st_mtime': 4.0},
    ]

    assert grouped_data[2] == [
        {'path': '5.1', 'st_mtime': 5.1},
        {'path': '5.9', 'st_mtime': 5.9},
    ]

    assert grouped_data[3] == [
        {'path': '7', 'st_mtime': 7.0},
        {'path': '8', 'st_mtime': 8.0},
        {'path': '9', 'st_mtime': 9.0},
    ]

    assert grouped_data[4] == [
        {'path': '11', 'st_mtime': 11.0}
    ]


def test_groupby_timestamp_can_group_large_distanced_data(monkeypatch):
    timestamps = [5.1, 0.5, 4, 7, 9, 5.9, 2, 8, 11, 1]
    data = list(map(lambda x: dict(path=str(x), st_mtime=float(x) * 1000), timestamps))
    grouped_data = groupby_timestamp(data, distance=1000)

    assert len(grouped_data) == 5
    assert grouped_data[0] == [
        {'path': '0.5', 'st_mtime': 500.0},
        {'path': '1', 'st_mtime': 1000.0},
        {'path': '2', 'st_mtime': 2000.0},
    ]

    assert grouped_data[1] == [
        {'path': '4', 'st_mtime': 4000.0},
    ]

    assert grouped_data[2] == [
        {'path': '5.1', 'st_mtime': 5100.0},
        {'path': '5.9', 'st_mtime': 5900.0},
    ]

    assert grouped_data[3] == [
        {'path': '7', 'st_mtime': 7000.0},
        {'path': '8', 'st_mtime': 8000.0},
        {'path': '9', 'st_mtime': 9000.0},
    ]

    assert grouped_data[4] == [
        {'path': '11', 'st_mtime': 11000.0}
    ]

def test_groupby_timestamp_filters_min_group_size():
    timestamps = [0,1,2, 4, 5.1,5.9, 7,8,9, 11]
    data = list(map(lambda x: dict(path=str(x), st_mtime=float(x)), timestamps))
    grouped_data = groupby_timestamp(data, distance=1, min_group_size=2)

    assert len(grouped_data) == 3
    assert grouped_data[0] == [
        {'path': '0', 'st_mtime': 0.0},
        {'path': '1', 'st_mtime': 1.0},
        {'path': '2', 'st_mtime': 2.0},
    ]

    assert grouped_data[1] == [
        {'path': '5.1', 'st_mtime': 5.1},
        {'path': '5.9', 'st_mtime': 5.9},
    ]

    assert grouped_data[2] == [
        {'path': '7', 'st_mtime': 7.0},
        {'path': '8', 'st_mtime': 8.0},
        {'path': '9', 'st_mtime': 9.0},
    ]

def test_as_transfer_list():
    grouped_data = [
        [
            {'path': Path('0'), 'st_mtime': 0.0},
            {'path': Path('1'), 'st_mtime': 1.0},
            {'path': Path('2'), 'st_mtime': 2.0},
        ],
        [
            {'path': Path('4'), 'st_mtime': 4.0},
        ],
        [
            {'path': Path('5.1'), 'st_mtime': 5.1},
            {'path': Path('5.9'), 'st_mtime': 5.9},
        ],
        [
            {'path': Path('7'), 'st_mtime': 7.0},
            {'path': Path('8'), 'st_mtime': 8.0},
            {'path': Path('9'), 'st_mtime': 9.0},
        ],
        [
            {'path': Path('11'), 'st_mtime': 11.0}
        ]
    ]

    dst_directory = Path('/destination')
    transfers = as_transfer_list(grouped_data, dst_directory)

    assert len(transfers) == 10
    assert transfers[0] == (Path('0') , Path('/destination/1970-01-01_00:00:00:::3/0'))
    assert transfers[1] == (Path('1') , Path('/destination/1970-01-01_00:00:00:::3/1'))
    assert transfers[2] == (Path('2') , Path('/destination/1970-01-01_00:00:00:::3/2'))

    assert transfers[3] == (Path('4') , Path('/destination/1970-01-01_00:00:04:::1/4'))

    assert transfers[4] == (Path('5.1') , Path('/destination/1970-01-01_00:00:05:::2/5.1'))
    assert transfers[5] == (Path('5.9') , Path('/destination/1970-01-01_00:00:05:::2/5.9'))

    assert transfers[6] == (Path('7') , Path('/destination/1970-01-01_00:00:07:::3/7'))
    assert transfers[7] == (Path('8') , Path('/destination/1970-01-01_00:00:07:::3/8'))
    assert transfers[8] == (Path('9') , Path('/destination/1970-01-01_00:00:07:::3/9'))

    assert transfers[9] == (Path('11') , Path('/destination/1970-01-01_00:00:11:::1/11'))

@mock.patch('group_closely_created_files.groupby_date.Path.mkdir')
@mock.patch('group_closely_created_files.groupby_date.move')
@mock.patch('group_closely_created_files.groupby_date.copy2')
def test_transfer(mocked_copy2, mocked_move, mocked_Path_mkdir):
    transfer_list = [
        (Path('0') , Path('/destination/1970-01-01_00:00:00:::3/0')),
    ]

    with raises(Exception):
        transfer(transfer_list, 'invalid')
    transfer(transfer_list, 'copy')

    mocked_copy2.assert_called_once_with(Path('0'), Path('/destination/1970-01-01_00:00:00:::3/0'))

    transfer(transfer_list, 'move')
    mocked_move.assert_called_once_with(Path('0'), Path('/destination/1970-01-01_00:00:00:::3/0'))




