from __future__ import with_statement
import sys
import zerorpc
import threading
from zerorpc.exceptions import LostRemote, TimeoutExpired


class MetricSingleton(type):
    _instance = {}
    """
        Metric Client Singelton Class Implementation
    """
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MetricSingleton, cls).__call__(
                *args)
        return cls._instance


class MetricClient(object):

    def __init__(self, host="127.0.0.1", port="13375"):
        if host != "" and port != "":
            self.sock = zerorpc.Client()
            self.sock.connect("tcp://{0}:{1}".format(host, port))
        else:
            raise SyntaxError

    def push(self, obj, value=False):
        """Set a set value."""
        try:
            self.sock.commit(obj, value)
        except (LostRemote, TimeoutExpired):
            e = sys.exc_info()
            print(e)
