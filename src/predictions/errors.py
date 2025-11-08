"""Module errors.py"""
import logging
import numpy as np
import pandas as pd

import src.elements.master as mr
import src.elements.structures as st
import src.elements.specification as sc
import src.predictions.persist


class Errors:
    """
    Calculates error measures & metrics, vis-à-vis predictions, (a) per instance of a gauge's data
    instances, and (b) across the instances of a gauge.
    """

    def __init__(self):
        """
        Constructor
        """

        # Quantile points
        self.__q_points = {0.10: 'l_whisker', 0.25: 'l_quartile', 0.50: 'median', 0.75: 'u_quartile', 0.90: 'u_whisker'}

        # Instances
        self.__persist = src.predictions.persist.Persist()

    @staticmethod
    def __get_errors(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: A training or testing data set.
        :return:
        """

        frame = data.copy()[['timestamp', 'measure', 'e_measure']]
        frame = frame.assign(ae=(frame['measure'] - frame['e_measure']).abs())
        frame.loc[:, 'ape'] = 100 * frame['ae'].divide(frame['measure']).values

        return frame

    def __get_quantiles(self, vector: np.ndarray) -> pd.DataFrame:
        """

        :param vector:
        :return:
        """

        quantiles = np.quantile(a=vector, q=list(self.__q_points.keys()), method='inverted_cdf').tolist()
        frame = pd.DataFrame(data=np.array([quantiles]), columns=list(self.__q_points.values()))

        return frame

    def exc(self, master: mr.Master, specification: sc.Specification) -> st.Structures:
        """

        :param master: Refer to src/elements/master.py
        :param specification:
        :return:
        """

        training = self.__get_errors(data=master.e_training)
        testing = self.__get_errors(data=master.e_testing)

        structures = st.Structures(
            training=training,
            testing=testing,
            q_training=self.__get_quantiles(vector=training['ape'].values),
            q_testing=self.__get_quantiles(vector=testing['ape'].values)
        )

        logging.info(structures.testing)
        logging.info(structures.q_testing)

        self.__persist.disaggregates(specification=specification, structures=structures)

        return structures
