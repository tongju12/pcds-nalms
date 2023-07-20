from pathlib import Path
from typing import List

import click
import pandas as pd


def check_duplicate_pvs(df: pd.DataFrame) -> List[str]:
    dup_column = df['PV'][df.duplicated('PV')].dropna()
    duplicates = dup_column.to_list() or []
    return duplicates


def check_blank_lines(df: pd.DataFrame) -> List[int]:
    cleaned_idx = df.dropna(how='all').index
    return [i for index, i in enumerate(df.index) if index not in cleaned_idx]


def validate_csvs(csv_dir: str):
    csv_dir = Path(csv_dir)

    fail = False
    for csv_file in csv_dir.glob('**/*.csv'):
        click.echo(f'validating {csv_file}...')
        csv_df = pd.read_csv(csv_file)
        duplicate_pvs = check_duplicate_pvs(csv_df)
        blank_line_nos = check_blank_lines(csv_df)

        if duplicate_pvs:
            click.echo(f'- found duplicate pvs: {duplicate_pvs}')
            fail = True

        if blank_line_nos:
            click.echo(f'- found blank lines: {blank_line_nos}')
            fail = True

    if fail:
        print('found csv validation failures')
        raise click.Abort()

    return

@click.command()
@click.argument('csv_dir', type=click.Path(exists=True))
def main(csv_dir):
    validate_csvs(csv_dir)

if __name__ == "__main__":
    main()

