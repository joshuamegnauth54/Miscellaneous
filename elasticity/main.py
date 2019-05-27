# -*- coding: utf-8 -*-

import pandas as pd

from elasticargs import create_args
from elasticargs import parse_args
from elasticprep import load_files
from elasticprep import partelast_colsplit


if __name__ == "__main__":
    varargs = create_args()
    parse_args(varargs)

    pe_merge = load_files(varargs)
    pe_merge = partelast_colsplit
