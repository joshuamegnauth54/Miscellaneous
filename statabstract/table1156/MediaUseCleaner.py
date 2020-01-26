# -*- coding: utf-8 -*-

import pandas as pd
import re
from collections import defaultdict
from typing import OrderedDict
from copy import deepcopy

from . import MUCData


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
        df.rename(columns=MUCData.columns, inplace=True)
        df = pd.melt(df, id_vars=["observation"], value_name="percent")
        df.variable = df.variable.astype("category")
        df.percent = pd.to_numeric(df.percent)
        df["year"] = int(year)

        return df

    def __gender(self, df: pd.DataFrame):
        """See documentation for __clean_dispatcher(MediaUseCleaner) for more
        information.

        Parameters
        ----------
        df: pandas.DataFrame
            Excel sheet from table1156.xls represented as a Pandas DataFrame.
        """
        genderdf = df.query(MUCData.qgender)

        if genderdf.empty:
            print(MUCData.nodata.format("Gender", df.year[0]))
            return

        genderdf.rename(columns={"observation": "gender"}, inplace=True)
        genderdf.gender = genderdf.gender.astype("category")

        self.__clean_dict["gender"] = pd.concat([self.__clean_dict["gender"],
                                                genderdf], ignore_index=True)

    def __age(self, df: pd.DataFrame):
        """See documentation for __clean_dispatcher(MediaUseCleaner) for more
        information.

        Parameters
        ----------
        df: pandas.DataFrame
            Excel sheet from table1156.xls represented as a Pandas DataFrame.
        """
        agedf = df.query(MUCData.qage)

        if agedf.empty:
            print(MUCData.nodata.format("Age", df.year[0]))
            return

        agedf.rename(columns={"observation": "age_years"}, inplace=True)
        agedf.age_years = agedf.age_years.map(MUCData.age_map)
        agedf.age_years = agedf.age_years.astype("category")

        self.__clean_dict["age"] = pd.concat([self.__clean_dict["age"],
                                             agedf], ignore_index=True)

    def __race(self, df: pd.DataFrame):
        """See documentation for __clean_dispatcher(MediaUseCleaner) for more
        information.

        Parameters
        ----------
        df: pandas.DataFrame
            Excel sheet from table1156.xls represented as a Pandas DataFrame.
        """
        racedf = df.query(MUCData.qrace)

        if racedf.empty:
            print(MUCData.nodata.format("Race", df.year[0]))
            return

        racedf.rename(columns={"observation": "race"}, inplace=True)
        racedf.race = racedf.race.map(MUCData.race_map)
        racedf.race = racedf.race.astype("category")
        self.__clean_dict["race"] = pd.concat([self.__clean_dict["race"],
                                              racedf], ignore_index=True)

    def __employment(self, df: pd.DataFrame):
        """See documentation for __clean_dispatcher(MediaUseCleaner) for more
        information.

        Parameters
        ----------
        df: pandas.DataFrame
            Excel sheet from table1156.xls represented as a Pandas DataFrame.
        """
        employdf = df.query(MUCData.qemploy)

        if employdf.empty:
            print(MUCData.nodata.format("Employment", df.year[0]))
            return

        employdf.rename(columns={"observation": "employment"}, inplace=True)
        employdf.employment = employdf.employment.map(MUCData.employ_map)
        employdf.employment = employdf.employment.astype("category")
        self.__clean_dict["employment"] = pd.concat([
                self.__clean_dict["employment"], employdf], ignore_index=True)

    def __income(self, df: pd.DataFrame):
        """See documentation for __clean_dispatcher(MediaUseCleaner) for more
        information.

        Parameters
        ----------
        df: pandas.DataFrame
            Excel sheet from table1156.xls represented as a Pandas DataFrame.
        """
        incomedf = df.query(MUCData.qincome)

        if incomedf.empty:
            print(MUCData.nodata.format("Income", df.year[0]))
            return

        incomedf.rename(columns={"observation": "income"}, inplace=True)
        incomedf.income = incomedf.income.map(MUCData.income_map)
        incomedf.income = incomedf.astype("category")
        self.__clean_dict["income"] = pd.concat([self.__clean_dict["income"],
                                                incomedf], ignore_index=True)

    def __school(self, df: pd.DataFrame):
        """See documentation for __clean_dispatcher(MediaUseCleaner) for more
        information.

        Parameters
        ----------
        df: pandas.DataFrame
            Excel sheet from table1156.xls represented as a Pandas DataFrame.
        """
        schooldf = df.query(MUCData.qeducation)

        if (schooldf.empty):
            print(MUCData.nodata.format("Education", df.year[0]))
            return

        schooldf.rename(columns={"observation": "school"}, inplace=True)
        schooldf.school = schooldf.school.map(MUCData.education_map)
        schooldf.school = schooldf.school.astype("category")

        self.__clean_dict["school"] = pd.concat([self.__clean_dict["school"],
                                                schooldf], ignore_index=True)

    def __init__(self, path: str):
        """Creates a cleaner for the Statistical Abstract's Table 1156.
        The data is split into multiple spreadsheets indexed by year with the
        current year labeled as 'Current.' As the Statistical Abstract consists
        mostly of summary tables, cleaning this data is more of a practice
        exercise with the added benefit that I can produce some neat charts
        out of it.

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
        self.__is_clean = False

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

    def __clean_dispatcher(self):
        """Calls each of the individual cleaning functions on each DataFrame.
        (Each DataFrame is an Excel sheet from the loaded data.)
        A general cleaning function is first called to spruce up the DataFrame
        before the individual cleaners can work with it.
        The individual cleaning functions each handle a different variable.
        Each function filters out observations pertaining to the specific
        variable into a new DataFrame. The resulting DataFrame has values
        renamed if necessary followed by being merged into a DataFrame that
        holds that variable.
        """
        for key, df in self.__unclean.items():
            df = self._clean_general_media(key, df)
            self.__gender(df)
            self.__age(df)
            self.__race(df)
            self.__employment(df)
            self.__income(df)
            self.__school(df)
        # We can presume cleaning succeeded if we reached this point (?)
        self.__is_clean = True

    def clean(self) -> OrderedDict[str, pd.DataFrame]:
        if self.__is_clean:
            return deepcopy(self.__clean_dict)
        else:
            raise RuntimeError(MUCData.cleanfailed.format(
                    self.__clean_dict.keys()))
