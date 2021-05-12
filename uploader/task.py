# ----
#     implements the use of output and requests in luigi.Task as
#     if they were descriptors using composition
#
#     classess:
#
#          Requirement
#          Requires
#          TargetOutput
# ----
from functools import partial
from hashlib import sha256

from luigi.local_target import LocalTarget
from luigi.target import Target
from luigi.task import Task
from luigi.task import flatten


class Requirement:
    """
    Descriptor to enable luigi to use more than one target
    as requires (see notes for lecture 6, page 48 for references)
    """
    def __init__(self, task_class, **params):
        self.task_class = task_class
        self.params = params

    def __get__(self, task: Task, cls) -> Task:
        # behaviour "return self if task is None" was introduced
        # during lecture 5. See page 36, Speaker notes.
        if task:
            return task.clone(self.task_class, **self.params)
        else:
            return self


class Requires:
    """
    Composition to replace :meth:`luigi.task.Task.requires`
    (see notes for lecture 6, page 48 for references)

    Example::
        class MyTask(Task):
            # Replace task.requires()
            requires = Requires()
            task1 = Requirement(Task1)
            task2 = Requirement(Task2)
            def run(self):
                # Convenient access here...
                with self.other.output().open('r') as f:
                    ...
            MyTask().requires()
        {'task1': Task1(), 'task2': Task2()}

    """

    def __get__(self, task, cls):
        # Bind self/task in a closure
        return partial(self.__call__, task)

    def __call__(self, task) -> dict:
        """Returns the requirements of a task
        Assumes the task class has :class:`.Requirement` descriptors, which
        can clone the appropriate dependences from the task instance.
        :returns: requirements compatible with `task.requires()`
        :rtype: dict
        """

        resq_tasks = [reqs for reqs, v in task.__class__.__dict__.items() if isinstance(v, Requirement)]
        return {req: getattr(task, req) for req in resq_tasks}


class TargetOutput:
    """
    Class composition to allow declare custom luigi targets
    with output as descriptor

    usage:  file_pattern = '{task.param1}/{task.param2}constant{ext}'
            param[i] = luigi.Param()
            ext = task.
            MyTask().output()
    """
    def __init__(
        self,
        file_pattern="{task.__class__.__name__}",
        ext=".csv",
        target_class=LocalTarget,
        **target_kwargs
    ):
        self.target_kwargs = target_kwargs
        self.file_pattern = file_pattern
        self.ext = ext
        self.target_class = target_class

    def __get__(self, task: Task, cls):
        """
        Part 1 of pattern "get__call":
        taking advantage of descriptor protocol, when
        the descriptor is called as method function then
        __call__ is invoked with the context of task,

        task: custom luigi task (instance)
        cls: custom luigi class
        """
        return partial(self.__call__, task)

    def __call__(self, task: Task) -> Target:
        """
        Part 2 of pattern "get__call":
        when __call__ is triggered by __get__
        then an output is formed according to the file_pattern
        and the parameters in task
        Reference: see slides for lecture 6, page 48

        task: custom luigi task (instance)
        """

        # file pattern contains the pattern, and task contains the parameters
        custom_format = self.file_pattern.format(task=task, self=self)
        return self.target_class(custom_format, **self.target_kwargs)


class SaltedOutput(TargetOutput):
    """
    "Salted Output": implementing SaltedGraph approach
    https://github.com/gorlins/salted/blob/master/salted.md
    """

    def __init__(self, file_pattern='{task.output_path}/{task.__class__.__name__}-{salt}',
                 ext=".csv",
                 target_class=LocalTarget,
                 **target_kwargs):
        self.file_pattern = file_pattern
        self.ext = ext
        self.target_class = target_class
        self.target_kwargs = target_kwargs

    def __call__(self, task: Task) -> Target:
        """
        Part 2 of pattern "get__call":
        when __call__ is triggered by __get__
        then an output is formed according to the file_pattern
        and the parameters in task
        Reference: see slides for lecture 6, page 48

        task: custom luigi task (instance)
        """

        # file pattern contains the pattern, and task contains the parameters
        custom_format = self.file_pattern.format(
            task=task,
            self=self,
            salt=self.get_salted_version(task)[:6])
        return self.target_class(custom_format, **self.target_kwargs)

    def get_salted_version(self, task):
        """
        From: https://github.com/gorlins/salted/blob/master/salted_demo.py
        Author: Scott Gorlin
        Create a salted id/version for this task and lineage
        :returns: a unique, deterministic hexdigest for this task
        :rtype: str
        """

        msg = ""

        # Salt with lineage
        for req in flatten(task.requires()):
            # Note that order is important and impacts the hash - if task
            # requirements are a dict, then consider doing this is sorted order
            msg += self.get_salted_version(req)

        # Uniquely specify this task
        msg += ','.join([

                # Basic capture of input type
                task.__class__.__name__,

                # Change __version__ at class level when everything needs rerunning!
                task.__version__,

            ] + [
                # Depending on strictness - skipping params is acceptable if
                # output already is partitioned by their params; including every
                # param may make hash *too* sensitive
                '{}={}'.format(param_name, repr(task.param_kwargs[param_name]))
                for param_name, param in sorted(task.get_params())
                if param.significant
            ]
        )
        return sha256(msg.encode()).hexdigest()
