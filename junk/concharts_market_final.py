# -*- coding: utf-8 -*-
"""Quick and dirty plots for my Data 735 final."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def platform_sales_data() -> pd.DataFrame:
    """Data from: https://www.vgchartz.com/analysis/platform_totals/
    https://www.popsci.com/ouyas-sale-end-crowdsourced-console/

    You shouldn't actually use this function for anything. I needed to make
    some quick and dirty charts for a project in a class.
    Returns
    -------
    pandas.DataFrame
        Returns a DataFrame with console sales data in millions.
    """

    consales = [{"Console": "PlayStation 4",
                 "Generation": 8,
                 "Sales": 109.05},
                {"Console": "Xbox One",
                 "Generation": 8,
                 "Sales": 47.19},
                {"Console": "Nintendo Switch",
                "Generation": 8,
                "Sales": 54.57},
                {"Console": "PlayStation Vita",
                 "Generation": 8,
                 "Sales": 16.21},
                {"Console": "Wii U",
                 "Generation": 8,
                 "Sales": 13.97},
                {"Console": "Nintendo 3DS",
                 "Generation": 8,
                 "Sales": 75.17},
                {"Console": "Ouya",
                 "Generation": 8,
                 "Sales": .2},
                {"Console": "PlayStation 3",
                 "Generation": 7,
                 "Sales": 87.41},
                {"Console": "Xbox 360",
                 "Generation": 7,
                 "Sales": 85.8,
                 "Generation": 7},
                {"Console": "Wii",
                 "Generation": 7,
                 "Sales": 101.64},
                {"Console": "PlayStation Portable",
                 "Generation": 7,
                 "Sales": 81.09},
                {"Console": "Nintendo DS",
                 "Generation": 7,
                 "Sales": 154.9}]

    sales_df = pd.DataFrame(consales)
    # Console generation is a factor not a number
    sales_df.Generation = sales_df.Generation.astype("category")
    return sales_df

def plat_sales_bar():
    return
