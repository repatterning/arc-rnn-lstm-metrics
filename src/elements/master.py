"""Module src.elements.master.py"""
import typing

import pandas as pd


class Master(typing.NamedTuple):
    """
    The data type class ⇾ Master<br><br>

    Attributes<br>
    ----------<br>
    e_training : pandas.DataFrame<br>
        The training data, and the target estimates vis-à-vis a model

    e_testing : pandas.DataFrame<br>
        The testing data, and the target estimates vis-à-vis the model
    """

    e_training: pd.DataFrame
    e_testing: pd.DataFrame
