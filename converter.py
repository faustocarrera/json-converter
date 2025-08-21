#!/usr/bin/env python3
"""
JSON to CSV Converter
Converts JSON files to CSV format using Click for command-line interface.
Supports both individual files and batch processing of folders.
"""

from pathlib import Path
import click
from jsonconverter import VerboseLogger
from jsonconverter import JSONconvert


@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.option('--recursive', '-r', is_flag=True, help='Process JSON files in subdirectories recursively')
@click.option('--output-dir', '-o', type=click.Path(path_type=Path), help='Output directory for CSV files (default: same as input)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def convert(input_path: Path, recursive: bool, output_dir: Path, verbose: bool):
    """
    Convert JSON files to CSV format.
    INPUT_PATH can be either a single JSON file or a directory containing JSON files.
    """
    converter = JSONconvert(input_path, recursive, output_dir, verbose)
    exported_files = converter.convert()
    print(exported_files)


if __name__ == '__main__':
    convert()
