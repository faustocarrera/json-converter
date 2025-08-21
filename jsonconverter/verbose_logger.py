#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verbose logging utility
"""


class VerboseLogger:
    "Verbose logger"
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def log(self, message: str):
        "Print message just if the verbose flag is set"
        if self.verbose:
            print(f"{message}")
