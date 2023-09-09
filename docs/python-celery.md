# Celery Integration

The Celery integration provides a task class that can be used to automatically create and update tasks in Task Badger
from Celery tasks.

The core API can be used to create and update tasks from any Celery task but the integration simplifies the usage.

At the core of the integration is the `taskbadger.Task` class which is a custom Celery task tells Task Badger that
the task should be tracked. The task class also provides convenient access to the Task Badger task object within the
body of the Celery task.

## Basic Usage
To use the integration simply set the `base` parameter of your Celery task to `taskbadger.Task`:

!!!note inline end ""

    This works the same with the `@celery.shared_task` decorator.

```python
from celery import Celery
from taskbadger.celery import Task

app = Celery("tasks")

@app.task(base=Task)
def my_task():
    pass

my_task.delay()
```

Having made this change, the task will now be automatically created in Task Badger when the task is called and
updated when the task completes.

!!! info

    Note that Task Badger will only track the Celery task if it is run asynchronously. If the task is run
    synchronously via `.apply()`, by calling the function directly, or if [`task_always_eager`][always_eager]{:target="_blank"} has been set,
    the task will not be tracked.


[always_eager]: https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_always_eager


## Task Customization

You can pass additional parameters to the Task Badger class which will be used when creating the task. This can be
done by passing keyword arguments prefixed with `taskbadger_` to the `.appy_async()` function or to the task
decorator.

```python
# using the task decorator

@app.task(base=Task, taskbadger_monitor_id="xyz")
def my_task(arg1, arg2):
    ...

# using individual keyword arguments
my_task.apply_async(
    arg1, arg2,
    taskbadger_name="my task",
    taskbadger_value_max=1000,
    taskbadger_data={"custom": "data"},
)

# using a dictionary
my_task.apply_async(arg1, arg2, taskbadger_kwargs={
    "name": "my task",
    "value_max": 1000,
    "data": {"custom": "data"}
})
```

!!!note "Order of Precedence"
    Values passed via `apply_async` take precedence over values passed in the task decorator.

    In both the decorator and `apply_async`, if individual keyword arguments are used as well as
    the `taskbadger_kwargs` dictionary, the individual arguments will take precedence.

## Accessing the Task Object

The `taskbadger.Task` class provides access to the Task Badger task object via the `taskbadger_task` property of the
Celery task. The Celery task instance can be accessed within a task function body by creating a
[bound task][bound_task]{:target="_blank"}.

[bound_task]: https://docs.celeryq.dev/en/stable/userguide/tasks.html#bound-tasks

```python
@app.task(bind=True, base=taskbadger.celery.Task)
def my_task(self, items):
    # Retrieve the Task Badger task
    task = self.taskbadger_task
    
    for i, item in enumerate(items):
        do_something(item)
    
        if i % 100 == 0:
            # Track progress
            task.update(value=i)
    
    # Mark the task as complete
    # This is normally handled automatically when the task completes but we call it here so that we
    # can also update the `value` property.
    task.success(value=len(items))
```

!!!note

    The `taskbadger_task` property will be `None` if the task is not being tracked by Task Badger.
    This could indicate that the Task Badger API has not been [configured](/python#configure), there was an error
    creating the task, or the task is being run synchronously e.g. via `.apply()` or calling the task
    using `.map` or `.starmap`, `.chunk`.
