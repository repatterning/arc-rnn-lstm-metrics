"""Module seasonal.py"""

import pandas as pd

import src.elements.master as mr
import src.elements.specification as sc
import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


class Data:
    """
    <b>Notes</b><br>
    ------<br>

    Retrieves the seasonal component forecasting estimations<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__streams = src.functions.streams.Streams()

    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: A uniform resource string
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    def exc(self, specification: sc.Specification) -> mr.Master:
        """

        :param specification: Refer to src/elements/specification.py
        :return:
        """

        return mr.Master(
            e_training=self.__get_data(uri=specification.uri + '/' + 'e_training.csv'),
            e_testing=self.__get_data(uri=specification.uri + '/' + 'e_testing.csv')
        )
