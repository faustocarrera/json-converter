#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List, Dict, Union, Any
import json

class SQLexport():
    "Export JSON to SQL files"

    def __init__(self, logger) -> None:
        self.logger = logger

    def export(self, data: Union[Dict, List], output_file: Path) -> bool:
        "Export data to SQL file"
        table_name = self.__get_table_name(output_file)
        columns = self.__get_columns(data)
        sql_script = self.__generate_sql_script(table_name, columns, data)
        self.logger.log(f"Exporting to {output_file}")
        # Write to output file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sql_script)
        return True

    def __get_table_name(self, output_file: Path) -> str:
        "Get the SQL table name from the output file name"
        return output_file.stem

    def __get_columns(self, data: Union[Dict, List]) -> dict:
        "Get columns and data types"
        columns = {}
        for record in data:
            for key, value in record.items():
                column_type = self.__infer_sql_type(value)
                if key not in columns:
                    columns[key] = column_type
                else: # Handle type conflicts by choosing more general type
                    if columns[key] != column_type:
                        columns[key] = self.__force_general_type(columns[key], column_type)
        return columns

    def __generate_sql_script(self, table_name: str, columns: dict, data: Union[Dict, List]) -> str:
        "Generate SQL script for creating table and inserting data"
        sql_script = f"CREATE TABLE {table_name} (\n"
        for column, col_type in columns.items():
            sql_script += f"  {column} {col_type},\n"
        sql_script = sql_script.rstrip(",\n") + "\n);\n\n"
        # Insert data
        for record in data:
            sql_script += f"INSERT INTO {table_name} ({', '.join(record.keys())}) VALUES ({', '.join(self.__format_value(v) for v in record.values())});\n"
        return sql_script

    @staticmethod
    def __format_value(value: Any) -> str:
        "Format a Python value for SQL insertion"
        formatted_value = f"'{str(value)}'"
        if value is None:
            formatted_value = "NULL"
        elif isinstance(value, bool):
            formatted_value = "TRUE" if value else "FALSE"
        elif isinstance(value, (int, float)):
            formatted_value = str(value)
        elif isinstance(value, str):
            # Escape single quotes by doubling them
            escaped = value.replace("'", "''")
            formatted_value = f"'{escaped}'"
        elif isinstance(value, (list, dict)):
            # Convert complex types to JSON strings
            json_str = json.dumps(value).replace("'", "''")
            formatted_value = f"'{json_str}'"
        return formatted_value

    @staticmethod
    def __infer_sql_type(value) -> str:
        "Infer SQL data type from Python value"
        sql_type = 'TEXT'
        if value is None:
            sql_type = 'TEXT'  # Default for NULL values
        elif isinstance(value, bool):
            sql_type = 'BOOLEAN'
        elif isinstance(value, int):
            sql_type = 'INTEGER'
        elif isinstance(value, float):
            sql_type = 'REAL'
        elif isinstance(value, str):
            # Use VARCHAR with reasonable length, or TEXT for longer strings
            sql_type = 'VARCHAR(255)' if len(value) <= 255 else 'TEXT'
        elif isinstance(value, (list, dict)):
            sql_type = 'TEXT'  # Store as JSON string
        return sql_type

    @staticmethod
    def __force_general_type(existing_type: str, current_type: str) -> str:
        "Force a more general SQL type in case of conflicts"
        sql_type = existing_type
        # Promote to more general type
        if existing_type == "INTEGER" and current_type == "REAL":
            sql_type = "REAL"
        elif existing_type == "REAL" and current_type == "INTEGER":
            pass  # Keep REAL
        elif "VARCHAR" in existing_type and current_type == "TEXT":
            sql_type = "TEXT"
        elif "VARCHAR" in current_type and existing_type == "TEXT":
            pass  # Keep TEXT
        return sql_type
