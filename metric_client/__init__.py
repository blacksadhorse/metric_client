from __future__ import absolute_import

from .client import MetricClient

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))
__all__ = ['MetricClient']
