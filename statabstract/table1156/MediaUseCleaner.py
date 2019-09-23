# -*- coding: utf-8 -*-

import pandas as pd
import re
from collections import defaultdict


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
                 "Accessed Internet": "internet_thirtydays"}
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
        df.rename(columns=MediaUseCleaner.__columns, inplace=True)
        df = pd.melt(df, id_vars=["observation"], value_name="frequency")
        df.variable = df.variable.astype("category")
        df.frequency = pd.to_numeric(df.frequency)
        df["year"] = int(year)

        return df

    def __gender(self, df: pd.DataFrame):
        gender = df.query("observation == 'Male' | observation == 'Female'")
        # This triggers a warning about setting a value on a copy, but that is
        # exactly what I want.
        gender.rename(columns={"observation": "gender"}, inplace=True)
        gender.gender = gender.gender.astype("category")

        self.__clean_dict["gender"] = pd.concat([self.__clean_dict["gender"],
                                                gender], ignore_index=True)

    def __age(self, df: pd.DataFrame):
        age = df.query("observation == '18 to 24 years old' |"
                       "observation == '25 to 34 years old' |"
                       "observation == '35 to 44 years old' |"
                       "observation == '45 to 54 years old' |"
                       "observation == '55 to 64 years old' |"
                       "observation == '65 years old and over'")

        age.rename(columns={"observation": "age_years"}, inplace=True)
        age.age_years = age.age_years.map({"18 to 24 years old": "18-24",
                                           "25 to 34 years old": "25-34",
                                           "35 to 44 years old": "35-44",
                                           "45 to 54 years old": "45-54",
                                           "55 to 64 years old": "55-64",
                                           "65 years old and over": "65+"})
        age.age = age.age.astype("category")

        self.__clean_dict["age"] = pd.concat([self.__clean_dict["age"],
                                             age], ignore_index=True)

    def __race(self, df: pd.DataFrame):
        racedf = df.query("observation == 'White only' | "
                          "observation == 'Black only' | "
                          "observation == 'Other races/multiple "
                          "classifications'")

        racedf.rename(columns={"observation": "race"}, inplace=True)
        racedf.race = racedf.race.map({"White only": "white",
                                       "Black only": "black",
                                       "Other races/multiple classifications":
                                           "other"})

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
        for key, df in self.__unclean.items():
            df = self._clean_general_media(key, df)
            self.__gender(df)
            self.__age(df)
            self.__race(df)
            self.__employment(df)
            self.__income(df)
