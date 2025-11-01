"""Module src.predictions.interface.py"""
import logging

import dask

import src.elements.master as mr
import src.elements.specification as sc
import src.elements.structures as st
import src.functions.directories
import src.predictions.data
import src.predictions.errors
import src.predictions.metrics


class Interface:
    """
    Interface
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(specifications: list[sc.Specification]):
        """

        :param specifications: An inventory
        :return:
        """

        __get_data = dask.delayed(src.predictions.data.Data().exc)
        __get_errors = dask.delayed(src.predictions.errors.Errors().exc)
        __get_metrics = dask.delayed(src.predictions.metrics.Metrics().exc)

        computations = []
        for specification in specifications:
            master: mr.Master = __get_data(specification=specification)
            structures: st.Structures = __get_errors(master=master)
            metrics = __get_metrics(structures=structures, specification=specification)
            computations.append(metrics)

        estimates = dask.compute(computations, scheduler='threads')[0]
        logging.info(estimates)

        elements = sum(estimates, [])
        logging.info(elements)
