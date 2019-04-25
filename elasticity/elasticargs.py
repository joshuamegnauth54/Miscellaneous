# -*- coding: utf-8 -*-

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
