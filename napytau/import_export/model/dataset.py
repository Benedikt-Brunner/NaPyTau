from dataclasses import dataclass

from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.relative_velocity import RelativeVelocity
from napytau.util.model.value_error_pair import ValueErrorPair


@dataclass
class DataSet:
    """
    A class to represent a dataset.
    A dataset represents the entirety of the data collected from a single observation.
    """

    relative_velocity: ValueErrorPair[RelativeVelocity]
    datapoints: DatapointCollection

    def get_relative_velocity(self) -> ValueErrorPair[RelativeVelocity]:
        return self.relative_velocity

    def get_datapoints(self) -> DatapointCollection:
        return self.datapoints
