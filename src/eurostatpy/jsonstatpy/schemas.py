import os
import json


class JsonStatSchema:
    def __init__(self):
        filename = os.path.join(os.path.dirname(
            __file__), "schemas", "jsonstat.json")
        with open(filename) as f:
            self.__all = json.loads(f.read())

        filename = os.path.join(os.path.dirname(
            __file__), "schemas", "collection.json")
        with open(filename) as f:
            self.__collection = json.loads(f.read())

        filename = os.path.join(os.path.dirname(
            __file__), "schemas", "dataset.json")
        with open(filename) as f:
            self.__dataset = json.loads(f.read())

        filename = os.path.join(os.path.dirname(
            __file__), "schemas", "dimension.json")
        with open(filename) as f:
            self.__dimension = json.loads(f.read())

    @property
    def dimension(self):
        return self.__dimension

    @property
    def dataset(self):
        return self.__dataset

    @property
    def collection(self):
        return self.__collection

    @property
    def all(self):
        return self.__all
