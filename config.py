"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>

        Over time, step-by-step, some of the items herein will be transferred to the overarching project's
        configurations zone/hub.

        """

        '''
        Keys
        '''
        self.architecture = 'arc-rnn-lstm'
        self.s3_parameters_key = 's3_parameters.yaml'
        self.argument_key = f'architectures/{self.architecture}/arguments.json'
        self.metadata_ = f'architectures/{self.architecture}/metrics/external'


        '''
        Project Metadata
        '''
        self.project_tag = 'hydrography'
        self.project_key_name = 'HydrographyProject'


        '''
        Local Paths
        '''
        self.data_ = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        self.pathway_ = self.warehouse
        self.points_ = os.path.join(self.pathway_, 'disaggregates', 'points')
        self.menu_ = os.path.join(self.pathway_, 'disaggregates', 'menu')
        self.aggregates_ = os.path.join(self.pathway_, 'aggregates')
