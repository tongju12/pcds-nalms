import shutil
from pathlib import Path

import click

from alarm_csv2xml import csvtoxml


def convert_csv_to_xml(indir, outdir):
    """
    Convert all CSV files in ``indir`` to XML.
    Mimicks the directory structure of ``indir`` in ``outdir``
    """
    indir = Path(indir)
    outdir = Path(outdir)
    click.echo(f'{indir}, {outdir}')

    shutil.rmtree(outdir, ignore_errors=True)
    outdir.mkdir()

    for fp in indir.glob('*'):
        if fp.is_dir():
            click.echo(f'-- recurse into {fp}, {outdir / fp.parent.name}')
            convert_csv_to_xml(str(fp), str(outdir / fp.name))
        elif fp.is_file() and fp.suffix == '.csv':
            click.echo(f'converting {fp} to {(outdir / fp.name).with_suffix(".xml")}')
            csvtoxml(fp, (outdir / fp.name).with_suffix(".xml"))
            ((outdir / fp.name).with_suffix('.xml')).touch()



@click.command()
@click.option('-i', '--indir', prompt='specify csv directory', required=True,
            type=str, help='path to CSV input file(s).')
@click.option('-o', '--outdir', default=None, required=False, type=str,
            help='path to XML output folder.')
def main_command(indir, outdir):
    convert_csv_to_xml(indir, outdir)


if __name__ == '__main__':
    main_command()