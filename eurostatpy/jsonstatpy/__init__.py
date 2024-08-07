from .exceptions import JsonStatException
from .exceptions import JsonStatMalformedJson

from .dimension import JsonStatDimension
from .value import JsonStatValue
from .dataset import JsonStatDataSet
from .collection import JsonStatCollection

import os
_examples_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "examples"))
