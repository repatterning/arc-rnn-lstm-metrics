"""Module interface.py"""
import logging

import pandas as pd

import src.data.cases
import src.data.menu
import src.data.reference
import src.data.specifications
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.elements.specification as sc


class Interface:
    """
    Interface
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self) -> list[sc.Specification]:
        """

        :return:
        """

        cases = src.data.cases.Cases(service=self.__service, s3_parameters=self.__s3_parameters).exc()

        # Reference
        reference: pd.DataFrame = src.data.reference.Reference(
            s3_parameters=self.__s3_parameters).exc(codes=cases['ts_id'].unique())
        reference = reference.copy().merge(cases, how='left', on=['catchment_id', 'ts_id'])

        # Menu
        src.data.menu.Menu().exc(reference=reference)

        # Specifications
        specifications: list[sc.Specification] = src.data.specifications.Specifications().exc(reference=reference)
        self.__logger.info(specifications)

        return specifications
