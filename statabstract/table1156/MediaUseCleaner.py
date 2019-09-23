# -*- coding: utf-8 -*-

import pandas as pd
import re
from collections import defaultdict

# =============================================================================
# To do:
# 1. Throw all of the query strings into their own class or load them from a
# text file.
# 2. Add more error checking/warnings.
# =============================================================================


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
                 "Accessed Internet": "internet_thirtydays",
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
        df.rename(columns=MediaUseCleaner.__columns, inplace=True)
        df = pd.melt(df, id_vars=["observation"], value_name="percent")
        df.variable = df.variable.astype("category")
        df.frequency = pd.to_numeric(df.frequency)
        df["year"] = int(year)

        return df

    def __gender(self, df: pd.DataFrame):
        genderdf = df.query("observation == 'Male' | observation == 'Female'")
        # This triggers a warning about setting a value on a copy, but that is
        # exactly what I want.
        genderdf.rename(columns={"observation": "gender"}, inplace=True)
        genderdf.gender = genderdf.gender.astype("category")

        self.__clean_dict["gender"] = pd.concat([self.__clean_dict["gender"],
                                                genderdf], ignore_index=True)

    def __age(self, df: pd.DataFrame):
        agedf = df.query("observation == '18 to 24 years old' | "
                         "observation == '25 to 34 years old' | "
                         "observation == '35 to 44 years old' | "
                         "observation == '45 to 54 years old' | "
                         "observation == '55 to 64 years old' | "
                         "observation == '65 years old and over'")

        agedf.rename(columns={"observation": "age_years"}, inplace=True)
        agedf.age_years = agedf.age_years.map({"18 to 24 years old": "18-24",
                                               "25 to 34 years old": "25-34",
                                               "35 to 44 years old": "35-44",
                                               "45 to 54 years old": "45-54",
                                               "55 to 64 years old": "55-64",
                                               "65 years old and over": "65+"})
        agedf.age_years = agedf.age_years.astype("category")

        self.__clean_dict["age"] = pd.concat([self.__clean_dict["age"],
                                             agedf], ignore_index=True)

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

        racedf.race = racedf.race.astype("category")
        self.__clean_dict["race"] = pd.concat([self.__clean_dict["race"],
                                              racedf], ignore_index=True)

    def __employment(self, df: pd.DataFrame):
        employdf = df.query("observation == '..Full time' | "
                            "observation == '..Part time' | "
                            "observation == 'Not employed'")
        employdf.rename(columns={"observation": "employment"}, inplace=True)
        employdf.employment = employdf.employment.map({"..Full time": "full",
                                                       "..Part time": "part",
                                                       "Not employed": "none"})

        employdf.employment = employdf.employment.astype("category")
        self.__clean_dict["employment"] = pd.concat([
                self.__clean_dict["employment"], employdf], ignore_index=True)

    def __income(self, df: pd.DataFrame):
        incomedf = df.query("observation == 'Less than $50,000' | "
                            "observation == '..$50,000 to $74,999' | "
                            "observation == '..$75,000 to $149,999' | "
                            "observation == '..$150,000 or more'")
        incomedf.rename(columns={"observation": "income"}, inplace=True)
        # Definitely need a better way to handle these strings
        tempmap = {"Less than $50,000": "<50000",
                   "..$50,000 to $74,999": "50000-74999",
                   "..$75,000 to $149,999": "75000-149999",
                   "..$150,000 or more": "150000+"}
        incomedf.income = incomedf.income.map(tempmap)
        incomedf.income = incomedf.astype("category")

        self.__clean_dict["income"] = pd.concat([self.__clean_dict["income"],
                                                incomedf], ignore_index=True)

    def __school(self, df: pd.DataFrame):
        schooldf = df.query("observation == 'Not high school graduate' | "
                            "observation == 'High school graduate' | "
                            "observation == 'Attend college' | "
                            "observation == 'College graduate'")

        if (schooldf.empty):
            # This is a verrryyyy temporary solution
            print("No school data: {}".format(df.year[0]))
            return

        schooldf.rename(columns={"observation": "school"}, inplace=True)
        tempmap = {"Not high school graduate": "no_highschool",
                   "High school graduate": "highschool",
                   "Attend college": "in_college",
                   "College graduate": "fin_college"}
        schooldf.school = schooldf.school.map(tempmap)
        schooldf.school = schooldf.school.astype("category")

        self.__clean_dict["school"] = pd.concat([self.__clean_dict["school"],
                                                schooldf], ignore_index=True)

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
            self.__school(df)
