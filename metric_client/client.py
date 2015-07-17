from __future__ import with_statement
import socket
import random
import sys
import time
from Queue import Queue
from threading import Thread


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
    __metaclass__ = MetricSingleton

    def __init__(self, host='localhost', port=13374, prefix=None,
                 maxudpsize=512, sleep=0.005):
        family, _, _, _, addr = socket.getaddrinfo(
            host, port, 0, socket.SOCK_DGRAM
        )[0]
        self._addr = addr
        self.sleep = sleep
        self._sock = socket.socket(family, socket.SOCK_DGRAM)
        self._prefix = prefix
        self._maxudpsize = maxudpsize
        self.q = Queue(maxsize=0)
        num_threads = 1
        for i in range(num_threads):
            worker = Thread(target=self.do_stuff, args=(self.q,))
            worker.setDaemon(True)
            worker.start()

    def push(self, obj, value=False):
        """Set a set value."""
        stat = ''
        if not value:
            value = time.time()
        count = len(obj)
        cur_count = 0
        for o in obj:
            cur_count += 1
            stat += str(o)+'%'+str(obj[o])
            if cur_count != count:
                stat += '.'
        try:
            self._send_stat(stat, '%s|s' % value, 1)
        except KeyboardInterrupt:
            e = sys.exc_info()
            print(e)

    def _send_stat(self, stat, value, rate):
        self._after(self._prepare(stat, value, rate))

    def _prepare(self, stat, value, rate):
        if rate < 1:
            if random.random() > rate:
                return
            value = '%s|@%s' % (value, rate)

        if self._prefix:
            stat = '%s.%s' % (self._prefix, stat)

        return '%s:%s' % (stat, value)

    def _after(self, data):
        if data:
            self.q.put(data)

    def do_stuff(self, f):
        while True:
            try:
                data = f.get()
                self._sock.sendto(data.encode('ascii'), self._addr)
                self.q.task_done()
                time.sleep(self.sleep)
            except socket.error:
                e = sys.exc_info()
                print(e)
