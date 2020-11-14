try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    pass

import sys

from . import helpers

from .day01 import puzzle1
from .day02 import puzzle2
from .day03 import puzzle3
from .day04 import puzzle4
from .day05 import puzzle5
from .day06 import puzzle6
from .day07 import puzzle7
from .day08 import puzzle8
from .day09 import puzzle9
from .day10 import puzzle10
from .day11 import puzzle11
from .day12 import puzzle12
from .day13 import puzzle13
from .day14 import puzzle14
from .day15 import puzzle15
from .day16 import puzzle16
from .day17 import puzzle17
from .day19 import puzzle19
from .day22 import puzzle22
from .day23 import puzzle23
from .day24 import puzzle24
