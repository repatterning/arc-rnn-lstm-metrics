"""Module src.elements.parts.py"""
import typing

import pandas as pd


class Structures(typing.NamedTuple):
    """
    The data type class ⇾ Structures<br><br>

    Attributes<br>
    ----------<br>
    training<br>
    testing<br>
    q_training<br>
    q_testing<br>
    """

    training: pd.DataFrame
    testing: pd.DataFrame
    q_training: pd.DataFrame
    q_testing: pd.DataFrame
