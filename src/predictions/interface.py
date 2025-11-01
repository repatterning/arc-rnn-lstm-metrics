"""Module src.predictions.interface.py"""
import logging

import dask

import config
import src.elements.master as mr
import src.elements.specification as sc
import src.elements.structures as st
import src.functions.directories
import src.predictions.data
import src.predictions.errors


class Interface:
    """
    Interface
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

    @staticmethod
    def exc(specifications: list[sc.Specification]):
        """

        :param specifications:
        :return:
        """

        __get_data = dask.delayed(src.predictions.data.Data().exc)
        __get_errors = dask.delayed(src.predictions.errors.Errors().exc)

        computations = []
        for specification in specifications:
            master: mr.Master = __get_data(specification=specification)
            structures: st.Structures = __get_errors(master=master)
            computations.append(structures.training.shape[0])

        messages = dask.compute(computations, scheduler='threads')[0]
        logging.info(messages)
