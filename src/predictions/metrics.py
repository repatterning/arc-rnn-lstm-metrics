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

        _se: np.ndarray = np.power(data['error'].to_numpy(), 2)
        _r_mean_se: float = np.sqrt(_se.mean())
        _r_median_se: float = np.sqrt(np.median(_se))

        return {'r_mean_se': float(_r_mean_se),
                'r_median_se': float(_r_median_se),
                'mean_pe': float(data['p_error'].mean()),
                'median_pe': float(data['p_error'].median()),
                'mean_e': float(data['error'].mean()),
                'median_e': float(data['error'].median()),
                'catchment_id': specification.catchment_id,
                'catchment_name': specification.catchment_name,
                'station_name': specification.station_name,
                'river_name': specification.river_name,
                'ts_id': specification.ts_id,
                'stage': stage}

    def exc(self, structures: st.Structures, specification: sc.Specification) -> list[dict]:
        """

        :param structures: An object of data frames vis-à-vis training & testing estimates, etc.
        :param specification:
        :return:
        """

        return [self.__metrics(data=structures.training, specification=specification, stage='training'),
                self.__metrics(data=structures.testing, specification=specification, stage='testing')]
