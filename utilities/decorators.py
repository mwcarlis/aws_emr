#!/usr/bin/python

def singleton(class_):
    """A singleton decorator.
    """
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class PoolLimitError(Exception):
    def __init__(self, msg):
        super(PoolLimitError, Exception).__init__()

class Pool(object):
    """A Base-Clase for object Pooling.
    """
    MAX = 10
    available = {}
    unavailable = {}
    pool_size = 0
    run_cnt = 0
    def __new__(class_, *args, **kwargs):
        """Maintain a Pool of instances with a MAX limit.

        Cases:
            1) Use an available instance from the Pool.
            2) Create a new instance for the Pool.
            3) No available instance and the Pool is at MAX:
                raise PoolLimitError('Too many kiddies in the pool.')
        """
        if len(class_.available) > 0:
            # There is available space in the Pool.
            class_.pool_id = class_.available.keys()[0]
            thing = class_.available.pop(class_.pool_id)
            thing.__jobid = class_.run_cnt
            class_.unavailable[thing.__jobid] = thing
            class_.run_cnt += 1
        elif class_.MAX > len(class_.available) + len(class_.unavailable):
            # Haven't hit the Pool Limit.
            # Allocate a new member of the Pool
            thing = object.__new__(class_, *args, **kwargs)
            thing.pool_id = class_.pool_size
            thing.__jobid = class_.run_cnt
            class_.unavailable[thing.__jobid] = thing
            class_.run_cnt += 1
            class_.pool_size += 1
        else:
            raise PoolLimitError('Not enough space in the pool')
        return thing

    def __del__(self):
        """Maintain the properties of a Pool for this instance.

        When we call __del__ we're going to keep the references as
        an available instance.  Pop out of the unavailable map and push
        into the available map.
        """
        print 'deleting'
        pid = self.pool_id
        self.available[pid] = self.unavailable.pop(self.__jobid)


