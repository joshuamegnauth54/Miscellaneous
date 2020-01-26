# -*- coding: utf-8 -*-

from typing import Dict

namemap = Dict[str, str]


class MUCData:
    __slots__ = ()

    columns = {"Item": "observation",
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

    # Query strings
    qgender: str = "observation == 'Male' | observation == 'Female'"
    qage: str = ("observation == '18 to 24 years old' | "
                 "observation == '25 to 34 years old' | "
                 "observation == '35 to 44 years old' | "
                 "observation == '45 to 54 years old' | "
                 "observation == '55 to 64 years old' | "
                 "observation == '65 years old and over'")
    qrace: str = ("observation == 'White only' | "
                  "observation == 'Black only' | "
                  "observation == 'Other races/multiple classifications'")
    qemploy: str = ("observation == '..Full time' | "
                    "observation == '..Part time' | "
                    "observation == 'Not employed'")
    qincome: str = ("observation == 'Less than $50,000' | "
                    "observation == '..$50,000 to $74,999' | "
                    "observation == '..$75,000 to $149,999' | "
                    "observation == '..$150,000 or more'")

    qeducation: str = ("observation == 'Not high school graduate' | "
                       "observation == 'High school graduate' | "
                       "observation == 'Attend college' | "
                       "observation == 'College graduate'")

    # Dictionaries to rename variables

    age_map: namemap = {"18 to 24 years old": "18-24",
                        "25 to 34 years old": "25-34",
                        "35 to 44 years old": "35-44",
                        "45 to 54 years old": "45-54",
                        "55 to 64 years old": "55-64",
                        "65 years old and over": "65+"}

    race_map: namemap = {"White only": "white",
                         "Black only": "black",
                         "Other races/multiple classifications": "other"}

    employ_map: namemap = {"..Full time": "full",
                           "..Part time": "part",
                           "Not employed": "none"}

    income_map: namemap = {"Less than $50,000": "<50000",
                           "..$50,000 to $74,999": "50000-74999",
                           "..$75,000 to $149,999": "75000-149999",
                           "..$150,000 or more": "150000+"}

    education_map: namemap = {"Not high school graduate": "no_highschool",
                              "High school graduate": "highschool",
                              "Attend college": "in_college",
                              "College graduate": "fin_college"}

    # Misc
    nodata: str = ("{} query returned an empty DataFrame for {}. Note: This is"
                   " usually not a major problem.")

    cleanfailed: str = ("Error: Cleaning did not succeed."
                        "Keys: %s")
