#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from pathlib import Path
import pandas as pd
from .csv_export import CSVexport
from .sql_export import SQLexport
from .verbose_logger import VerboseLogger


class JSONconvert():
    "Convert JSON files to other formats"

    def __init__(self, input_path, recursive=False, output_dir=None, format='csv', verbose=False) -> None:
        self.input_path = input_path
        self.recursive = recursive
        self.output_dir = output_dir
        self.format = format
        self.logger = VerboseLogger(verbose)

    def convert(self) -> list:
        "Perform the conversion"
        self.logger.log(f"Starting conversion for: {self.input_path}")
        self.logger.log('Get the JSON list of files')
        # get json files
        json_files = self.__get_json_files(self.input_path, self.recursive)
        # log the number of json files found
        if self.logger:
            self.logger.log(f"Found {len(json_files)} JSON files")
        # output dir
        if self.output_dir:
            self.__make_output_dir(self.output_dir)
        # flatten the json files
        exported_files = self.__export_json_data(json_files)
        # check the files
        self.logger.log(f"Exported {len(exported_files)} files to CSV format")
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

    def __export_json_data(self, json_files: list) -> list:
        "Read and flatten JSON files"
        exporter = self.__get_exporter()
        exported_files = []
        for file in json_files:
            with open(file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                flattened_data = self.__flatten_json(json_data)
                if self.format == 'csv':  # export csv
                    output_file = self.__get_output_filename(file, '.csv')
                    if exporter.export(flattened_data, output_file):
                        exported_files.append(output_file.absolute())
                if self.format == 'sql':
                    output_file = self.__get_output_filename(file, '.sql')
                    if exporter.export(flattened_data, output_file):
                        exported_files.append(output_file.absolute())
        return exported_files

    def __flatten_json(self, json_data: dict) -> list:
        "Flatten JSON data"
        return pd.json_normalize(json_data, sep='.').to_dict(orient='records')

    @staticmethod
    def __make_output_dir(output_dir: Path) -> None:
        "Create destination"
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

    def __get_output_filename(self, json_file: Path, ext: str) -> Path:
        "Get csv file path"
        csv_filename = json_file.name.replace('.json', ext)
        if self.output_dir:
            return self.output_dir / csv_filename
        return Path(csv_filename)

    def __get_exporter(self):
        "Get the appropriate exporter class"
        if self.format == 'csv':
            return CSVexport(self.logger)
        if self.format == 'sql':
            return SQLexport(self.logger)
        raise ValueError(f"Unsupported format: {self.format}")
