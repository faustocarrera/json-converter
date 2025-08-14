JSON files converter
=========================

This README provides an overview of the **JSON Converter**, a script designed to streamline data conversion. The primary goal of this tool is to provide a fast and dependable solution for transforming data from JSON format to a different outputs.

## What It Does

The **JSON Converter** takes a structured, valid JSON input, flatten the structure and exports it. It's designed to handle csv and database outputs, making it a versatile tool for developers, data analysts, and anyone who needs to transform data from JSON format.

## Key Features:

- **Click-based CLI** with intuitive command-line interface
- **Flexible input:** Accepts both individual JSON files and directories
- **Automatic file discovery:** Finds all .json files in a directory
- **Smart JSON handling:** Processes different JSON structures (arrays, objects, simple values)
- **Nested structure flattening:** Automatically flattens nested JSON objects (can be disabled)
- **Error handling:** Graceful handling of invalid JSON and file errors

## How it works:

- **JSON Detection:** Automatically finds JSON files based on file extension
- **Structure Analysis:** Handles different JSON formats (arrays of objects, single objects, simple values)
- **Flattening:** Converts nested JSON structures to flat CSV columns (e.g., user.address.city)
- **CSV Generation:** Creates CSV files with the same base name as the JSON files
- **Error Reporting:** Provides clear feedback on conversion success/failure

The script intelligently handles various JSON structures and creates well-formatted CSV files that preserve all the data from your JSON files.

## Getting Started

Install all the required libraries.

```bash
pip install -r requirements.txt
```

## Usage


```bash
python json-converter.py myfile.json
python json-converter.py ./inputfolder
python json-converter.py ./inputfolder --output-dir ./outputfolder
python json-converter.py ./inputfolder --verbose
```

---

## Contributing

We welcome contributions! If you'd like to improve the **JSON Converter** or report an issue, please see our contributing guidelines.

---

## License

This project is licensed under the GPL license - see the LICENSE.md file for details.
