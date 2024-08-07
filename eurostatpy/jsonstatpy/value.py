from collections import namedtuple


class JsonStatValue(namedtuple('JsonStatValue', ['idx', 'value', 'status'])):
    """Represents a value (datapoint) contained into JsonStatDataset"""
    pass
