# -*- coding: utf-8 -*-

import pandas as pd
import re
from collections import defaultdict

"""
General process:
    1. Drop nulls
    2. Strip Item
    3. Set Item to Index
    4. Slice each variable (i.e. ages)
    5.
"""


class MediaUseCleaner:

    def _clean_general_media(self, year: str,
                             df: pd.DataFrame) -> pd.DataFrame:
        """Performs general cleaning operations for each spreadsheet.

        Parameters
        ----------
        year: str
            String representing df's year. This should be the key to df's
            value.

        df: pandas.DataFrame
            Single sheet of a Table 1156 xls file as a DataFrame.

        Operations
        ----------
        1. The only nulls are the rows that were used as line breaks. Dropping
        all nulls in this case is entirely fine.
        2. The 'Item" column seems to have stray trailing spaces that must be
        removed.
        3. Some of the column titles have \\n, \\1, and \\2 between words or
        at the end of the line. These are replaced and the trailing white
        space is removed.
        """
        df.dropna(inplace=True)
        df.Item = df.Item.str.strip()
# =============================================================================
#         The incorrect characters are replaced with spaces to avoid butchering
#         the columns with '\\n' between words.
# =============================================================================
        df.columns = df.columns.str.replace(self._col_regex, " ")
        df.columns = df.columns.str.strip()

        return df

    def __init__(self, path: str):
        """Creates a cleaner for the Statistical Abstract's Table 1156.
        The data is split into multiple spreadsheets indexed by year with the
        current year labeled as 'Current.'

        My cleaner returns a dictionary with the observational units as keys
        and the DataFrames as values.
        Keys: age, gender, race, education, employed, and income

        Parameters
        ----------
        path: string
            Path to a Table 1156 xls.
        """
        self._unclean = pd.read_excel(path, header=2, sheet_name=None)
        self._clean_dict = {}
        self._col_regex = re.compile(r"[\n|\\1|\\2]+")
        self._columns = {"}

        years_range = sorted(self._unclean.keys())  # Note: keys are the years
        last_object = years_range[-1]  # Should be 'Current'
        try:
            # Add one to the last real year to get the current year if the
            # last year is 'Current.'
            year_end = (int(years_range[-2]) + 1
                        if last_object == "Current"
                        else int(last_object))
            self._unclean[year_end] = self._unclean.pop(last_object)
        except ValueError:
            print("WARNING: Expected an integer or 'Current'; got {}"
                  .format(last_object))
        self._clean_dispatcher()

    def _clean_dispatcher(self) -> pd.DataFrame:
        for key, df in self._unclean.items():
            self._clean_general_media(key, df)

