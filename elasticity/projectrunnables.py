# -*- coding: utf-8 -*-

from elasticargs import create_args
from elasticargs import parse_args
from elasticprep import load_files
from elasticprep import partelast_colsplit


def create_pe_dataframe():
    arguments = parse_args(create_args())
    pe_merge = partelast_colsplit(load_files(arguments))

    return pe_merge
