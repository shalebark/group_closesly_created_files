from pathlib import Path
from itertools import groupby
from datetime import datetime
from shutil import copy2, move

def read_dir(source: Path):
    files = [file for file in source.glob('*') if file.is_file()]
    return [{'path': file.resolve(), 'st_mtime': file.stat().st_mtime} for file in files]

# dir_data: Iterable
def groupby_timestamp(dir_data, distance=120, min_group_size=1):
    dir_data.sort(key=lambda x: x['st_mtime'])

    class Eq:
        def __init__(self, v):
            self.v = v['st_mtime']
        def __eq__(self, b):
            is_equal = abs(self.v - b.v) <= distance
            if is_equal:
                self.v = b.v
            return is_equal

    return list(filter(lambda g: len(g) >= min_group_size, [list(b) for _, b in groupby(dir_data, key=Eq)]))

def as_transfer_list(groups, destination: Path):
    transfers = []
    for group in groups:
        main = group[0]
        folder_name = datetime.utcfromtimestamp(main['st_mtime']).strftime('%Y-%m-%d_%H:%M:%S') + ':::' + str(len(group))

        for item in group:
            transfers.append((item['path'], destination / folder_name / item['path'].name))

    return transfers

def transfer(transfer_list, method='copy'):
    methods = {'copy': copy2, 'move': move}
    methodfnc = methods[method]

    for transfer in transfer_list:
        transfer[1].parent.mkdir(exist_ok=True, parents=True)
        methodfnc(*transfer)

