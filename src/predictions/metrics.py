"""Module metrics.py"""
import typing

import numpy as np
import pandas as pd

import src.elements.specification as sc
import src.elements.structures as st


class Metrics:
    """
    Metrics
    """

    def __init__(self):
        pass

    @staticmethod
    def __metrics(data: pd.DataFrame, specification: sc.Specification, stage: typing.Literal['training', 'testing']) -> dict:
        """

        :param data: A frame of measures, estimates, and errors
        :param specification:
        :param stage: The data of the training or testing stage
        :return:
        """

        _se: np.ndarray = np.power(data['ae'].to_numpy(), 2)
        _r_mse: float = np.sqrt(_se.mean())

        return {'rmse': float(_r_mse),
                'mape': float(data['ape'].mean()),
                'mae': float(data['ae'].mean()),
                'catchment_id': specification.catchment_id,
                'ts_id': specification.ts_id,
                'stage': stage}

    def exc(self, structures: st.Structures, specification: sc.Specification) -> list[dict]:
        """

        :param structures: An object of data frames vis-à-vis training & testing estimates, etc.
        :param specification:
        :return:
        """

        return [self.__metrics(data=structures.training, specification=specification, stage='training'),
                self.__metrics(data=structures.training, specification=specification, stage='testing')]
