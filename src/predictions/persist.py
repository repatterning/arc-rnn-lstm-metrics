"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.elements.specification as sc
import src.elements.structures as st
import src.functions.objects
import src.predictions.sections
import src.predictions.stages


class Persist:
    """
    Persist
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # An instance for writing JSON objects
        self.__objects = src.functions.objects.Objects()

    def __persist(self, nodes: dict | list[dict], path: str) -> str:
        """

        :param nodes: Dictionary of data.
        :param path: ...
        :return:
        """

        return self.__objects.write(nodes=nodes, path=path)

    @staticmethod
    def __get_node(blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        string: str = blob.to_json(orient='split')

        return json.loads(string)

    def disaggregates(self, specification: sc.Specification, structures: st.Structures) -> str:
        """

        :param specification: <br>
        :param structures: <br>
        :return:
        """

        nodes = {
            'training': self.__get_node(structures.training),
            'testing': self.__get_node(structures.testing),
            'q_training': self.__get_node(structures.q_training),
            'q_testing': self.__get_node(structures.q_testing)
        }
        nodes.update(specification._asdict())
        nodes.pop('uri', None)

        path = os.path.join(self.__configurations.points_, f'{str(specification.ts_id)}.json')

        return self.__persist(nodes=nodes, path=path)

    def aggregates(self, frame: pd.DataFrame) -> str:
        """

        :param frame:
        :return:
        """

        catchments = frame[['catchment_id', 'catchment_name']].drop_duplicates()

        nodes = {}
        for catchment_id, catchment_name in zip(catchments['catchment_id'].to_list(), catchments['catchment_name'].to_list()):
            excerpt: pd.DataFrame = frame.copy().loc[frame['catchment_id'] == catchment_id, :]
            node = src.predictions.stages.Stages(excerpt=excerpt).__call__()
            node['catchment_id'] = catchment_id
            node['catchment_name'] = catchment_name
            nodes[int(catchment_id)] = node
        path = os.path.join(self.__configurations.aggregates_, 'aggregates.json')

        return self.__persist(nodes=nodes, path=path)
