"""A Scheduler object.
"""
from collections import namedtuple
import heapq as minheap

from decorators import singleton




# A Schedule Job object.
SchdJob = namedtuple('Job', ['job', 'number', 'priority'])

@singleton
class RoundRobinAction(object):
    """A stateless queue action management class
    """
    def push(self, queue, job_obj):
        number = job_obj.number
        queue.append((number, job_obj))
    def pop(self, queue):
        number, job_obj = queue.pop(0)
        return job_obj
    def action(self, queue):
        # We don't have arrival order anymore..
        for cnt, val in enumerate(queue):
            magnitude, job_obj = val
            n_val = (job_obj.number, job_obj)
            queue[cnt] = n_val
        queue.sort()

@singleton
class PriorityAction(object):
    """A stateless queue action management class
    """
    def push(self, queue, job_obj):
        priority = job_obj.priority
        minheap.heappush(queue, (priority, job_obj))
    def pop(self, queue):
        priority, job_obj = minheap.heappop(queue)
        return job_obj
    def action(self, queue):
        for cnt, val in enumerate(queue):
            magnitude, job_obj = val
            n_val = (job_obj.priority, job_obj)
            queue[cnt] = n_val
        minheap.heapify(queue)

def _default_val_if(mapping, key):
    try:
        item = mapping[key]
    except KeyError as excp:
        item = mapping['default']
    return item

class Scheduler(object):
    SCHEDULE_FUNCS = {}
    QUEUE_FUNCS = {}
    INSERT_FUNCS = {}
    def __init__(self, schedule_type='roundrobin'):
        self.num_jobs = 0
        self.queue = []
        self.schedule_type = None
        self.set_schedule_type(schedule_type)

    def set_schedule_type(self, schedule_type):
        """Set the schedule algorithm type..
        """
        if schedule_type != self.schedule_type:
            self.schedule_type = schedule_type
            self.queue_action = self.QUEUE_FUNCS[schedule_type]
            self.schedule = _default_val_if(self.SCHEDULE_FUNCS, schedule_type)
            self.job_scheduler = _default_val_if(self.INSERT_FUNCS, schedule_type)
            self.queue_action.action(self.queue)

    def _default_pop_loop(self):
        while len(self.queue) > 0:
            job_obj = self.queue_action.pop(self.queue)
            yield job_obj.job

    def _push_job(self, job, priority):
        """Add a job to the schedule.

        Result:
            A Job is now added to the schedule.
        """
        # The queue is of (sort_order, job_obj)
        self.num_jobs += 1
        job_obj = SchdJob(job, self.num_jobs, priority=priority)
        self.queue_action.push(self.queue, job_obj)

    def schedule_job(self, job, priority=0):
        self.job_scheduler(self, job, priority)

    def scheduling(self):
        """Get the next item from the scheduler.
        """
        for blob in self.schedule(self):
            yield blob

    # What functions do we have to determine
    # Schedule priority/fairness/schedule_type?
    QUEUE_FUNCS = {
        'roundrobin': RoundRobinAction(),
        'priority': PriorityAction()
    }
    SCHEDULE_FUNCS = {
        ## Override the default if necessary
        'default': _default_pop_loop,
    }
    INSERT_FUNCS = {
        ## Override the default if necessary
        'default': _push_job,
    }
    def __contains__(self):
        return False

def insert_test_sequence(schd):
    schd.schedule_job(15, 15)
    schd.schedule_job('Z','Z')
    schd.schedule_job('C','C')
    schd.schedule_job('A','A')
    schd.schedule_job(10, 10)
    schd.schedule_job(0, 0)
    schd.schedule_job('O', 'O')

if __name__ == '__main__':
    schd = Scheduler('priority')
    insert_test_sequence(schd)
    for job in schd.scheduling():
        print job

