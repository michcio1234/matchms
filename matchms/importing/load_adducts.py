import os
from functools import lru_cache
from typing import Dict
import yaml
import pandas as pd


@lru_cache(maxsize=4)
def load_adducts_dict(filename: str = None) -> Dict:
    """Load dictionary of known adducts. Makes sure that file loading is cached.

    Parameters
    ----------
    filename:
        Yaml file containing adducts.
    """
    if filename is None:
        known_adducts_file = os.path.join(os.path.dirname(__file__), "..", "data", "known_adducts.yaml")
    else:
        known_adducts_file = filename

    if os.path.isfile(known_adducts_file):
        with open(known_adducts_file, 'r') as f:
            known_adducts = yaml.safe_load(f)
    else:
        print("Could not find yaml file with known adducts.")
        known_adducts = {'adducts_positive': [],
                         'adducts_negative': []}

    return known_adducts


@lru_cache(maxsize=4)
def load_adducts_table(filename: str = None) -> Dict:
    """Load table of known adducts and their charges and masses.
    Makes sure that file loading is cached.

    Parameters
    ----------
    filename:
        .csv file containing adducts.
    """
    if filename is None:
        adducts_file = os.path.join(os.path.dirname(__file__), "..", "data", "known_adducts_table.csv")
    else:
        adducts_file = filename

    if os.path.isfile(adducts_file):
        adducts_table = pd.read_csv(adducts_file)
    else:
        print("Could not find csv file with adducts table.")
        adducts_table = None

    return adducts_table
