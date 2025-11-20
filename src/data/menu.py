"""Module menu.py"""
import logging
import os

import pandas as pd

import config
import src.functions.objects


class Menu:
    """
    Menu
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

    def __persist(self, nodes: dict | list[dict], path: str):
        """

        :param nodes:
        :param path:
        :return:
        """

        message = self.__objects.write(nodes=nodes, path=path)
        logging.info('Graphing Menu ->\n%s', message)

    def __aggregates(self, excerpt: pd.DataFrame):
        """

        :param excerpt:
        :return:
        """


        frame = excerpt.copy()[['catchment_id', 'catchment_name']].drop_duplicates()
        frame.rename(columns={'catchment_id': 'desc', 'catchment_name': 'name'}, inplace=True)
        nodes = frame.to_dict(orient='records')
        logging.info(nodes)

        # Persist
        path = os.path.join(self.__configurations.aggregates_, 'catchments.json')
        self.__persist(nodes=nodes, path=path)

    def __disaggregates(self, excerpt: pd.DataFrame):
        """

        :param excerpt:
        :return:
        """

        names = (excerpt['station_name'] + '/' + excerpt['catchment_name']).to_numpy()
        frame = pd.DataFrame(data={'desc': excerpt['ts_id'].to_numpy(),
                                   'name': names})
        nodes = frame.to_dict(orient='records')
        logging.info(nodes)

        # Persist
        path = os.path.join(self.__configurations.menu_, 'menu.json')
        self.__persist(nodes=nodes, path=path)

    def exc(self, reference: pd.DataFrame):
        """

        :param reference: The reference sheet of the water level gauges.
        :return:
        """

        # Sort
        excerpt = reference.copy().sort_values(by=['catchment_name', 'station_name'], ascending=True)
        self.__disaggregates(excerpt=excerpt.copy())
        self.__aggregates(excerpt=excerpt.copy())
