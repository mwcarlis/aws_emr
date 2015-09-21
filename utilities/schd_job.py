#!/usr/bin/python

import time
import threading
import random

from mr_job import MRWordFreqCount

class SchdJob(object):
    """An abstract Schedule Job class capable of taking an action().
    """
    def action(self):
        """Take an action()
        """
        raise Exception('UnImplemented')

    def __enter__(self):
        raise Exception('UnImplemented')
    def __exit__(self, ttype, value, traceback):
        raise Exception('UnImplemented')

class MrSchdJob(threading.Thread, SchdJob):
    """Take a MrJob Action.
    """
    def __init__(self):
        super(MrSchdJob, self).__init__()
        self.alive = threading.Event()

    def _run_aws(self, path):
        cnt = 0
        while self.alive.isSet():
            try:
                cnt += 1
                # output_path = 's3://facedata/out2/trash{}'.format(path)
                # output_arg = '--output_dir={}'.format(output_path)
                # arguments = ['-r', 'emr', 'input/stanford_article.txt', output_arg]
                # job_obj = MRWordFreqCount(args=arguments)

            except Exception:
                self.alive.clear()
                break
        print cnt


    def run(self):
        for attempt in xrange(100):
            try:
                self._run_aws(attempt)
            except IOError, excp:
                if 'Output path' in excp.message and 'already exists' in excp.message:
                    # This bucket already exists, try another one.
                    continue
                # We don't know what this exception is, re-raise it.
                raise
            break

    def action(self):
        self.alive.set()
        self.start()

    def __enter__(self):
        self.action()
        return 'status action'
    def __exit__(self, ttype, value, traceback):
        self.alive.clear()

class TestIterT(threading.Thread):
    def __init__(self):
        super(TestT, self).__init__()
        self.alive = threading.Event()
        self.finished = False
        self.queue = []

    def run(self):
        for val in range(20):
            rsecs = float(random.randint(5, 50)) / 100.0
            time.sleep(rsecs)
            self.queue.append(val * 2)
        self.finished = True
        self.alive.clear()

    def __iter__(self):
        self.alive.set()
        self.start()
        while not self.finished or len(self.queue) != 0:
            while not self.finished and len(self.queue) == 0:
                time.sleep(0.025)
            if len(self.queue) == 0:
                continue
            yield self.queue.pop(0)


def test_tt():
    print 'start test_tt'
    tt = TestIterT()
    for val in tt:
        print val
    print 'end test_tt\n\n'

def test_schdjb():
    print 'start test_schdjb'
    schdj = MrSchdJob()
    with schdj as status:
        for _x in range(1000):
            pass
        schdj.alive.clear()
    time.sleep(0.5)
    print 'end test_schdjb\n\n'

if __name__ == '__main__':
    test_tt()
    test_schdjb()

