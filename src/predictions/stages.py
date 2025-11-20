"""Module sections.py"""
import json

import pandas as pd


class Stages:
    """
    This class creates training, testing, etc., sections.
    """

    def __init__(self, excerpt: pd.DataFrame):
        """

        :param excerpt: A frame of metrics per gauge.
        """

        self.__excerpt = excerpt
        self.__stages = self.__excerpt['stage'].unique()

    def __get_disaggregate(self, stage: str) -> dict:
        """

        :param stage: e,g., training, testing, etc.
        :return:
        """

        latest: pd.DataFrame = self.__excerpt.copy().loc[self.__excerpt['stage'] == stage, :]
        latest.drop(columns='stage', inplace=True)
        string = latest.to_json(orient='split')
        values = json.loads(string)

        return values

    def __call__(self):
        """

        :return:
        """

        computation = {stage: self.__get_disaggregate(stage=stage) for stage in self.__stages}

        return computation
