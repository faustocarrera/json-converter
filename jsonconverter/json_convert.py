#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from pathlib import Path
import pandas as pd
from .exporter.csv_export import CSVexport
from .exporter.sql_export import SQLexport
from .exporter.xml_export import XMLexport
from .verbose_logger import VerboseLogger


class JSONconvert():
    "Convert JSON files to other formats"

    def __init__(self, verbose=False) -> None:
        self.logger = VerboseLogger(verbose)
        self.supported_formats = ['csv', 'sql', 'xml']

    def convert(self, input_path: Path, output_dir: Path, output_format: str = 'csv', recursive=False) -> list:
        "Perform the conversion"
        self.logger.log(f"Starting conversion for: {input_path}")
        self.logger.log('Get the JSON list of files')
        # force output format to lower case
        output_format = output_format.lower()
        # check the output format
        if output_format not in self.supported_formats:
            print(f"Error: Unsupported output format '{output_format}'. Supported formats are: {', '.join(self.supported_formats)}")
            sys.exit(1)
        # get json files
        json_files = self.__get_json_files(input_path, recursive)
        # log the number of json files found
        if self.logger:
            self.logger.log(f"Found {len(json_files)} JSON files")
        # output dir
        if output_dir:
            self.__make_output_dir(output_dir)
        # flatten the json files
        exported_files = self.__export_json_data(
            json_files, output_format, output_dir)
        # check the files
        self.logger.log(
            f"Exported {len(exported_files)} files to {output_format} format")
        self.logger.log("Conversion complete")
        return exported_files

    def __get_json_files(self, input_path: Path, recursive: bool) -> list:
        json_files = []
        if input_path.is_file():
            if input_path.suffix.lower() != '.json':
                print("Error: Input file must have .json extension")
                sys.exit(1)
            json_files = [input_path]
        elif input_path.is_dir():
            if recursive:
                json_files = list(input_path.rglob('*.json'))
            else:
                json_files = self.__find_json_files(input_path)
            # no json files found
            if not json_files:
                print(f"No JSON files found in {input_path}")
                sys.exit(1)
        else:
            print(f"Error: {input_path} is neither a file nor a directory")
            sys.exit(1)
        return json_files

    @staticmethod
    def __find_json_files(path: Path) -> list:
        "Find all JSON files in a directory (non-recursive)"
        try:
            return [f for f in os.scandir(path) if f.is_file() and f.name.lower().endswith('.json')]
        except OSError as e:
            print(f"Error reading directory {path}: {e}")
            return []

    def __export_json_data(self, json_files: list, output_format: str, output_dir: Path) -> list:
        "Read and flatten JSON files"
        exporter = self.__get_exporter(output_format)
        exported_files = []
        for file in json_files:
            with open(file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                flattened_data = self.__flatten_json(json_data)
                output_file = self.__get_output_filename(
                    output_dir,
                    file,
                    f".{output_format}"
                )
                if exporter.export(flattened_data, output_file):
                    exported_files.append(output_file.absolute())
        return exported_files

    def __flatten_json(self, json_data: dict) -> list:
        "Flatten JSON data"
        return pd.json_normalize(json_data, sep='.').to_dict(orient='records')

    @staticmethod
    def __make_output_dir(output_dir: Path) -> None:
        "Create destination directory if it doesn't exist"
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

    def __get_output_filename(self, output_dir: Path, json_file: Path, ext: str) -> Path:
        "Get output file path"
        output_filename = json_file.name.replace('.json', ext)
        if output_dir:
            return output_dir / output_filename
        return Path(output_filename)

    def __get_exporter(self, output_format: str):
        "Get the appropriate exporter class"
        if output_format == 'csv':
            return CSVexport(self.logger)
        if output_format == 'sql':
            return SQLexport(self.logger)
        if output_format == 'xml':
            return XMLexport(self.logger)
        raise ValueError(f"Unsupported format: {output_format}")
