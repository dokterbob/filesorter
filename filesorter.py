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

import sys, argparse, os, re, logging, mimetypes, shutil, time
from datetime import datetime, timedelta

# Default logger
logger = logging.getLogger('filesorter')

# Ignore these files
IGNORE_FILENAMES = (
    re.compile('^\.'),
)

# Explicitly add AVCHD
mimetypes.add_type('video/avchd', '.mts')
mimetypes.add_type('video/avchd', '.m2ts')

MIN_AGE = timedelta(minutes=5)


def ignore_filename(filename):
    """ Whether or not to ignore a specific path. """
    for regex in IGNORE_FILENAMES:
        if regex.search(filename):
            return True
    return False


def sort_files(path, dest, dry_run=False):
    now = datetime.now()

    logger.info('Processing %s', path)

    if dry_run:
        print 'dry run'

    for (dirpath, dirnames, filenames) in os.walk(path):
        # logger.debug('dirpath: %s, dirnames: %s, filenames: %s', dirpath, dirnames, filenames)

        dirmtime = datetime.fromtimestamp(os.path.getmtime(dirpath))

        delta = now - dirmtime
        if delta < MIN_AGE:
            logger.warn('Directory %s modified too recently, skipping (%s minute(s) ago)',
                        dirpath, int(delta.total_seconds()/60))
            continue

        for filename in filenames:
            if ignore_filename(filename):
                logger.info('Ignoring %s', filename)
                continue

            fullpath = os.path.join(dirpath, filename)
            logger.debug('Processing: %s', fullpath)
            
            # Determine file change date
            mtime = datetime.fromtimestamp(os.path.getmtime(fullpath))
            
            delta = now - mtime
            if delta < MIN_AGE:
                logger.warn('File %s modified too recently, skipping (%s minute(s) ago)',
                            fullpath, int(delta.total_seconds()/60))
                continue
                
            datestr = mtime.date().isoformat()

            (mimetype, enoding) = mimetypes.guess_type(filename)

            if not mimetype:
                logger.warn('Mimetype for %s could not be determined', filename)
                main_type = 'Unknown'
            else:
                logger.debug('Mimetype: %s', mimetype)
                main_type = mimetype.split('/')[0].title()
            
            # Replace 'Application' with 'Unknown'
            if main_type == 'Application':
                main_type = 'Unknown'

            logger.debug('Main type: %s', main_type)

            new_filename = os.path.join(dest, datestr, main_type, dirpath[len(path):], filename)

            logger.info('Renaming %s to %s', fullpath, new_filename)

            if not dry_run:
                # shutil.move(src, dst)

                logger.debug('Attempting to remove directory %s', dirpath)
                
                try:
                    os.rmdir(dirpath)
                except OSError:
                    logger.warn('Cannot unlink %s; not empty', dirpath)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Sort and order the files in a directory by date and filetype.')
    parser.add_argument('path', metavar='<pathname>', type=str)
    parser.add_argument('--dest', '-d', metavar='<dest>', type=str)
    parser.add_argument('--dry-run', '-n', help='Show what would have been done.', action='store_true')
    parser.add_argument('--logging', '-l', help='Log level.', type=str, default='info', choices=('debug', 'info', 'warn', 'error'))
    args = parser.parse_args()

    numeric_level = getattr(logging, args.logging.upper())
    logging.basicConfig(level=numeric_level, format='%(message)s')

    # if not args.dest:
    #     args.dest = args.path

    sort_files(args.path, args.dest or args.path, args.dry_run)

if __name__ == "__main__":
    sys.exit(main())
