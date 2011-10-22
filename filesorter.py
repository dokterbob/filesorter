#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Mathijs de Bruin on 2011-10-22.
Copyright (c) 2011 mathijsfietst.nl. All rights reserved.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
COPYING for more details. 
"""

import sys
import getopt


help_message = '''
The help message goes here.
'''


def sort_files(path, dry_run=False):
    if dry_run:
        print 'dry run'
    print path

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description='Sort and order the files in a directory by date and filetype.')
    parser.add_argument('path', metavar='<pathname>', type=str, )
    parser.add_argument('--dry-run', help='Show what would have been done.', action='store_true')

    args = parser.parse_args()

    sort_files(args.path, args.dry_run)

if __name__ == "__main__":
    sys.exit(main())
