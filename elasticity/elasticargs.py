# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
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

    datasetlnks = ET.parse("datasets.xml").getroot()
    argumentsdict = vars(arguments)

    for key, value in argumentsdict.items():
        if not value:
            argumentsdict[key] = (datasetlnks.findall('.//dataset[@name="' +
                                                      key + '"]/url')[0].text)
