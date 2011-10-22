#!/usr/bin/env python
# encoding: utf-8
"""
filesorter.py

Created by Mathijs de Bruin on 2011-10-22.
Copyright (c) 2011 mathijsfietst.nl. All rights reserved.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
COPYING for more details. 
"""

import sys, argparse, os, re, logging, mimetypes


logger = logging.getLogger('filesorter')


IGNORE_PATHS = (
    re.compile('^\.'),
)

def ignore_path(path):
    """ Whether or not to ignore a specific path. """
    for regex in IGNORE_PATHS:
        if regex.search(path):
            return True
    return False


def sort_files(path, dry_run=False):
    logger.info('Processing %s', path)

    if dry_run:
        print 'dry run'

    for filename in os.listdir(path):
        if ignore_path(filename):
            logger.info('Ignoring %s', filename)
            continue

        logger.debug('Processing %s', filename)
        
        
    

def main(argv=None):
    parser = argparse.ArgumentParser(description='Sort and order the files in a directory by date and filetype.')
    parser.add_argument('path', metavar='<pathname>', type=str)
    parser.add_argument('--dry-run', '-n', help='Show what would have been done.', action='store_true')
    parser.add_argument('--logging', '-l', help='Log level.', type=str, default='info', choices=('debug', 'info', 'warn', 'error'))
    args = parser.parse_args()

    numeric_level = getattr(logging, args.logging.upper())
    logging.basicConfig(level=numeric_level, format='%(message)s')

    sort_files(args.path, args.dry_run)

if __name__ == "__main__":
    sys.exit(main())
