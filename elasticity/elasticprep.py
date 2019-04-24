# -*- coding: utf-8 -*-

import pandas as pd
from argparse import ArgumentParser


def create_args():
    """
    Creates an ArgumentParser and sets the valid inputs.
    The logic here is that the caller may wish to override the paths for
    the required datasets.
    """
    varargs = ArgumentParser()

    varargs.add_argument("-partisan", help="Override the path for the "
                                           "Partisan Leaning dataset "
                                           "(FiveThirtyEight)")

    varargs.add_argument("-elastic", help="Override the path for the "
                                          " Elasticity dataset "
                                          "(FiveThirtyEight)")

    return varargs.parse_args()


def parse_args(arguments):
    """
    In this function we check if the caller overrode any of the arguments.
    If not, we set the defaults.

    :param arguments: An argparse.Namespace with the following attributes;
    partisan, elastic
    """

    # To-do: I'd rather load these from a file instead of hardcoding URLs
    if not arguments.partisan:
        arguments.partisan = "https://github.com/fivethirtyeight/data/raw/master/partisan-lean/fivethirtyeight_partisan_lean_DISTRICTS.csv"

    if not arguments.elastic:
        arguments.elastic = "https://github.com/fivethirtyeight/data/raw/master/political-elasticity-scores/elasticity-by-district.csv"


def load_files(overrides):
    """
    """

# =============================================================================
#     We set the index to district to easily merge the DataFrames.
#     Also, we convert district to a category variable because it's more
#     efficient to work with and uses less memory than strings.
# =============================================================================
    pdist = pd.read_csv(overrides.partisan, index_col="district",
                        dtype={"district": "category"})

    edist = pd.read_csv(overrides.elastic, index_col="district",
                        dtype={"district": "category"})

    # Merge on indexes, sort our indexes, and try not to copy
    pe_merge = pdist.merge(edist, left_index=True, right_index=True,
                           sort=True, copy=False)

    return pe_merge

