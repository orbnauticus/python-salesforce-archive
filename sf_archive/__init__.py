"""
Inspect Salesforce data exports
"""


import csv
import os
import tempfile
import zipfile

from . import schema

import logging
try:
    import logcolors
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=logcolors.handlers(),
    )
except ImportError:
    logging.basicConfig(
        level=logging.DEBUG,
    )


class SalesforceArchive:
    """
    Salesforce data export
    """

    @classmethod
    def extract(cls, archive_path, extract_path=None):
        """
        Unpack a zip archive
        """
        if extract_path is None:
            extract_path = tempfile.TemporaryDirectory().name
        logging.debug('Extracting archive %r to %r',
                      archive_path, extract_path)
        zip_archive = zipfile.ZipFile(archive_path)
        zip_archive.extractall(extract_path)
        return cls(extract_path)

    def __init__(self, root):
        logging.debug('Reading file structure at %r', root)
        self.root = root
        self.tables = dict()
        root_listing = [
            (path[:-4], os.path.join(self.root, path))
            for path in os.listdir(self.root) if path.endswith('.csv')]
        for table, path in root_listing:
            if table not in schema.schema:
                continue
            self.tables[table] = Table(table, path)


class Table:
    def __init__(self, name, path, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", *args, **kwds):
        self._fieldnames = fieldnames   # list of keys for the dict
        self.restkey = restkey          # key to catch long rows
        self.restval = restval          # default value for short rows
        self.reader = csv.reader(open(path), dialect, *args, **kwds)
        self.dialect = dialect
        self.line_num = 0
        self.schema = schema.get(name, {None: str})

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            try:
                self._fieldnames = next(self.reader)
            except StopIteration:
                pass
        self.line_num = self.reader.line_num
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def __next__(self):
        if self.line_num == 0:
            # Used only for its side effect.
            self.fieldnames
        row = next(self.reader)
        self.line_num = self.reader.line_num

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = next(self.reader)
        default_xform = self.schema['DataTypes'].get(None, str)
        d = {key: self.schema['DataTypes'].get(key, default_xform)(value)
             for key, value in zip(self.fieldnames, row)}
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d

__all__ = ['SalesforceArchive']
