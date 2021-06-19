import click
from pathlib import Path
from group_closely_created_files.groupby_date import read_dir, groupby_timestamp, as_transfer_list, transfer

@click.command()
@click.argument('src_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True, path_type=Path))
@click.argument('dst_directory', type=click.Path(exists=False, file_okay=False, dir_okay=True, writable=True, resolve_path=True, path_type=Path))
@click.option('-d', '--time-difference', type=int, default=120)
@click.option('-m', '--method', type=click.Choice(['copy', 'move']), default='copy')
@click.option('-n', '--min-group-size', type=int, default=1)
def cli(src_directory, dst_directory, time_difference, method, min_group_size):
    data = read_dir(src_directory)
    groups = groupby_timestamp(data, time_difference, min_group_size)
    transfers = as_transfer_list(groups, dst_directory)
    transfer(transfers, method)

if __name__ == '__main__':
    cli()