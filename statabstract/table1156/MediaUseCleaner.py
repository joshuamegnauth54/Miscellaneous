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
    __columns = {"Item": "observation",
                 "Total population ( ,000)": "total_pop",
                 "Television viewing": "tv",
                 "Television prime time viewing": "tv_prime",
                 "Cable/pay TV viewing": "cable",
                 "Cable TV viewing": "cable",
                 "Cable viewing": "cable",
                 "Radio listening": "radio",
                 "Newspaper reading": "newspaper",
                 "Internet use": "internet",
                 "Internet use in past 30 days": "internet_thirtydays",
                 "Accessed internet": "internet_thirtydays"}
#    __format_base = "observation == '{}'"

#    def _query_string(self) -> str:
#        pass

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
        space is removed. My ReGex is a bit buggy, so it also breaks the Total
        Population columns. (Oops.) My code reflects the broken column name.
        Regardless, I drop that column as the user can just sum the other
        columns if a total is needed.
        4. The columns are renamed to be usable (i.e., less words, no spaces,
        and no caps). Some of the internet columns are measured in terms of
        internet use within the last thirty days. These are coalsced into
        one column.
        5. A molten DataFrame is created to ease the next cleaning step.
        6. Columns are given new types.
        7. A year column is added to ease building the new DataFrames.
        """
        df.dropna(inplace=True)
        df.Item = df.Item.str.strip()
# =============================================================================
#         The incorrect characters are replaced with spaces to avoid butchering
#         the columns with '\\n' between words.
# =============================================================================
        df.columns = df.columns.str.replace(self.__col_regex, " ")
        df.columns = df.columns.str.strip()
        df.drop(columns=["Total population ( ,000)"], inplace=True)
        df.rename(columns=MediaUseCleaner._columns, inplace=True)
        df = pd.melt(df, id_vars=["observation"], value_name="frequency")
        df.variable = df.variable.astype("category")
        df.value = pd.to_numeric(df.value)
        df["year"] = int(year)

        return df

    def __gender(self, df: pd.DataFrame):
        gender = df.query("observation == 'Male' | observation == 'Female'")
        # This triggers a warning about setting a value on a copy, but that is
        # exactly what I want.
        gender.rename(columns={"observation": "gender"}, inplace=True)
        gender.set_index("variable", inplace=True)

        self.__clean_dict["gender"] = self.__clean_dict["gender"].append(
                gender)

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
        self.__unclean = pd.read_excel(path, header=2, sheet_name=None)
        self.__clean_dict = defaultdict(pd.DataFrame)
        self.__col_regex = re.compile(r"[\n|\\1|\\2]+")  # I hate RegEx

        years_range = sorted(self.__unclean.keys())  # Note: keys are the years
        last_object = years_range[-1]  # Should be 'Current'
        try:
            # Add one to the last real year to get the current year if the
            # last year is 'Current.'
            year_end = (int(years_range[-2]) + 1
                        if last_object == "Current"
                        else int(last_object))
            self.__unclean[year_end] = self.__unclean.pop(last_object)
        except ValueError:
            print("WARNING: Expected an integer or 'Current'; got {}"
                  .format(last_object))
        self.__clean_dispatcher()

    def __clean_dispatcher(self) -> pd.DataFrame:
        for key, df in self._unclean.items():
            self._clean_general_media(key, df)
            self.__gender(df)
