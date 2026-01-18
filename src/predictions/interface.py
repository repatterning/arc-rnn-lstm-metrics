"""Module src.predictions.interface.py"""
import logging

import dask
import pandas as pd

import src.elements.master as mr
import src.elements.specification as sc
import src.elements.structures as st
import src.functions.directories
import src.predictions.data
import src.predictions.errors
import src.predictions.persist
import src.predictions.statements


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__persist = src.predictions.persist.Persist()

    def exc(self, specifications: list[sc.Specification]):
        """

        :param specifications: An inventory
        :return:
        """

        __get_data = dask.delayed(src.predictions.data.Data().exc)
        __get_errors = dask.delayed(src.predictions.errors.Errors().exc)
        __get_statements = dask.delayed(src.predictions.statements.Statements().exc)

        computations = []
        for specification in specifications:
            master: mr.Master = __get_data(specification=specification)
            structures: st.Structures = __get_errors(master=master, specification=specification)
            statements = __get_statements(structures=structures, specification=specification)
            computations.append(statements)

        elements: list[list[dict]] = dask.compute(computations, scheduler='threads')[0]
        __parts: list[dict] = sum(elements, [])
        frame = pd.DataFrame.from_records(data=__parts)

        # persist: statements
        message = self.__persist.statements(frame=frame)
        logging.info(message)

        # persist: aggregates
        message = self.__persist.aggregates(frame=frame)
        logging.info(message)
