# -*- coding: utf-8 -*-

import pandas as pd


def partelast_colsplit(pe_merge):
    """
    """
# =============================================================================
#    The pvi_538 column is an unwieldly string. I split it into two columns:
#    'party' and 'partisanlean.' The columns need to actually be named as
#    'expand=True' assigns numerical column names by default.
#    Lastly, the columns are typecast from string objects to be easier to use
#    and more efficient.
# =============================================================================
    pe_merge = pe_merge.merge(pe_merge.pvi_538.str.split("+", expand=True),
                              left_index=True, right_index=True, copy=False)

    pe_merge.columns = ["elasticity", "party", "partisanlean"]

    pe_merge.party = pe_merge.party.astype("category")
    pe_merge.partisanlean = pe_merge.partisanlean.apply(pd.to_numeric)

    # Finally, delete the old column and return the reference.
    del pe_merge["pvi_538"]
    return pe_merge


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

