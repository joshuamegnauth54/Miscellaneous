# -*- coding: utf-8 -*-

import pandas as pd

from elasticargs import create_args
from elasticargs import parse_args
from elasticprep import load_files


if __name__ == "__MAIN__":
    pe_merge = None
    varargs = create_args()
    parse_args(varargs)

    pe_merge = load_files(varargs)