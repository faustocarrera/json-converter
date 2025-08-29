#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON to XML Converter
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import List, Dict, Union


class XMLexport():
    "Export JSON to XML files"

    def __init__(self, logger) -> None:
        self.logger = logger

    def export(self, data: Union[Dict, List], output_file: Path) -> bool:
        "Export data to XML file"
        root = ET.Element(output_file.stem)

        if isinstance(data, dict):
            for key, value in data.items():
                self.__add_element(root, key, value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self.__add_element(root, f"item_{i}", item)
        else:
            root.text = str(data) if data is not None else ""
            if data is None:
                root.set("null", "true")

        self.logger.log(f"Exporting to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self.__prettify_xml(root))
        return True

    def __add_element(self, parent, key, value):
        "Add an element to the parent based on value type."
        # Handle invalid XML tag names
        if not key or not isinstance(key, str):
            key = 'item'

        # Replace invalid characters in tag names
        key = ''.join(c if c.isalnum() or c in '_-.' else '_' for c in key)
        if key[0].isdigit():
            key = 'item_' + key

        elem = ET.SubElement(parent, key)

        if isinstance(value, dict):
            for k, v in value.items():
                self.__add_element(elem, k, v)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                self.__add_element(elem, f"item_{i}", item)
        elif value is None:
            elem.set('null', 'true')
        elif isinstance(value, bool):
            elem.text = str(value).lower()
        else:
            elem.text = str(value)

        return elem

    @staticmethod
    def __prettify_xml(element):
        "Return a pretty-printed XML string for the Element."
        rough_string = ET.tostring(element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")[23:]  # Remove XML declaration
