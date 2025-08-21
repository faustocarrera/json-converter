#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from pathlib import Path
from typing import List, Dict, Union


class CSVexport():
    "Export JSON to CSV files"

    def __init__(self, logger) -> None:
        self.logger = logger

    def export(self, data: Union[Dict, List], output_file: Path) -> bool:
        "Export data to CSV file"
        # Handle different JSON structures
        if not data:
            print(f"Warning: {output_file} empty array")
            return False
        if isinstance(data, list):
            rows = []
            for item in data:
                rows.append(item if isinstance(item, dict) else {'value': item})
            # Get all unique keys for headers
            all_keys = set()
            for row in rows:
                all_keys.update(row.keys())
            fieldnames = sorted(all_keys)
        elif isinstance(data, dict):
            rows = [data]
            fieldnames = sorted(data.keys())
        else:
            # Simple value
            rows = [{'value': data}]
            fieldnames = ['value']

        # Write CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                # Fill missing keys with empty strings
                complete_row = {key: row.get(key, '') for key in fieldnames}
                writer.writerow(complete_row)
        return True
