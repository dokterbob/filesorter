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


IGNORE_FILENAMES = (
    re.compile('^\.'),
)

def ignore_filename(filename):
    """ Whether or not to ignore a specific path. """
    for regex in IGNORE_FILENAMES:
        if regex.search(filename):
            return True
    return False


def sort_files(path, dry_run=False):
    logger.info('Processing %s', path)

    if dry_run:
        print 'dry run'

    for (dirpath, dirnames, filenames) in os.walk(path):
        logger.debug('dirpath: %s, dirnames: %s, filenames: %s', dirpath, dirnames, filenames)
        
        for filename in filenames:
            if ignore_filename(filename):
                logger.info('Ignoring %s', filename)
                continue
        
            logger.debug('Processing %s', filename)
        
            (mimetype, enoding) = mimetypes.guess_type(filename)
            
            if not mimetype:
                logger.warn('Mimetype for %s could not be determined', filename)
            else:
                logger.debug('Mimetype: %s', mimetype)
            
            main_type = mimetype.split('/')[0].title()
            logger.debug('Main type: %s', main_type)
    

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
