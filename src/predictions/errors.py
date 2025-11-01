"""Module errors.py"""
import logging

import pandas as pd

import src.elements.master as mr
import src.elements.structures as st


class Errors:
    """
    Errors
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_errors(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: A training or testing data set.
        :return:
        """

        frame = data.copy()[['measure', 'e_measure']]
        frame = frame.assign(ae=(frame['measure'] - frame['e_measure']).abs())
        frame.loc[:, 'ape'] = 100 * frame['ae'].divide(frame['measure']).values

        logging.info(frame)

        return frame

    def exc(self, master: mr.Master) -> st.Structures:
        """

        :param master: Refer to src/elements/master.py
        :return:
        """

        structures = st.Structures(
            training=self.__get_errors(data=master.e_training),
            testing=self.__get_errors(data=master.e_testing))

        return structures
