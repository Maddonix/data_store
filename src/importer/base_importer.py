from collections import namedtuple

import_tuple = namedtuple(
    "ImportTuple",
    ["data_object", "data", "labels", "config"],
)


class BaseImporter:
    def __init__(self):
        self.id = None

    def set_id(self, id: int):
        self.id = id

    def save_datapoint(self, engine, data_tuple):
        pass
