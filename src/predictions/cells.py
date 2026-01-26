"""Module structure.py"""
import json

import dask
import pandas as pd


class Structure:
    """
    This class structures the metrics data.
    """

    def __init__(self, instances: pd.DataFrame):
        """

        :param instances: Data instances.
        """

        self.__instances = instances

    @dask.delayed
    def __get_node(self, data: pd.DataFrame, catchment_id: int, catchment_name: str) -> dict:
        """

        :param data:
        :param catchment_id: The identification code of a catchment area.
        :param catchment_name: The name of a catchment area.
        :return:
        """


        string: str = data.to_json(orient='split')
        node = json.loads(string)
        node['catchment_id'] = catchment_id
        node['catchment_name'] = catchment_name

        return node

    @dask.delayed
    def __get_data(self, catchment_id: int) -> pd.DataFrame:
        """

        :param catchment_id: The identification code of a catchment area.
        :return:
        """

        return self.__instances.copy().loc[
               self.__instances['catchment_id'] == catchment_id, :]

    def exc(self):
        """

        :return:
        """

        parts = self.__instances.copy()[['catchment_id', 'catchment_name']].drop_duplicates(ignore_index=True)
        parts.set_index(keys='catchment_id', inplace=True)

        # Hence, a dictionary whereby the keys -> `catchment code`, and values -> `catchment names`
        catchments: dict = parts.to_dict(orient='dict')['catchment_name']

        # Compute
        computations = []
        for catchment_id, catchment_name in catchments.items():
            data = self.__get_data(catchment_id=catchment_id)
            node = self.__get_node(data=data, catchment_id=catchment_id, catchment_name=catchment_name)
            computations.append(node)

        elements = dask.compute(computations, scheduler='threads')[0]

        return elements
