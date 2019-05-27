# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from argparse import ArgumentParser


def create_args():
    """Creates an ArgumentParser and sets the valid inputs.
    The logic here is that the caller may wish to override the paths for
    the required datasets.
    """
    varargs = ArgumentParser()

    partisan_help = ("Override the default path to FiveThirtyEight's "
                     "Partisan Leaning dataset.")
    varargs.add_argument("-p", "--partisan", help=partisan_help)

    elastic_help = ("Override the default path to FiveThirtyEight's "
                    "Elasticity dataset.")
    varargs.add_argument("-e", "--elastic", help=elastic_help)

    return varargs.parse_args()


def parse_args(arguments):
    """In this function we check if the caller overrode any of the arguments.
    If not, we set the defaults.

    :param arguments: An argparse.Namespace with the following attributes:
    partisan, elastic
    """
# =============================================================================
#     Load the file with the default paths to the datasets (datasets.xml).
#     We also need to create a dictionary to loop over from our arguments.
#
#     If no path is set in our arguments object, we use the dictionary key
#     which is also the 'name' attribute of the dataset tag to get the default
#     path. Look at datasets.xml if this is confusing.
# =============================================================================

    datasetlnks = ET.parse("datasets.xml").getroot()
    argumentsdict = vars(arguments)

    for key, value in argumentsdict.items():
        if not value:
            argumentsdict[key] = (datasetlnks.findall('.//dataset[@name="' +
                                                      key + '"]/url')[0].text)
