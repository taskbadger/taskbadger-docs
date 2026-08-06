# Celery Integration

The Celery integration provides a task class that can be used to automatically create and update tasks in Task Badger
from Celery tasks. Although you can use the basic SDK functions to create and update tasks from Celery tasks, the
Celery integration simplifies the usage significantly.

There are two ways you can use the Celery integration:

1. Use the `CelerySystemIntegration` to automatically track all Celery tasks.
2. Use the `taskbadger.celery.Task` class as the base class for Celery tasks you wish to track.

You can use both mechanisms at the same time since the base class is useful if you want to access to the
Task Badger task object within the body of the Celery task.

## Celery System Integration

If you want to track all tasks, you can use the `CelerySystemIntegration` class. By default, this will track every
task that is executed by the Celery workers (except the internal Celery tasks), including periodic / scheduled tasks.

```python
import taskbadger
from taskbadger.systems import CelerySystemIntegration

taskbadger.init(
    token="YOUR_API_KEY",
    systems=[CelerySystemIntegration()],
    tags={"environment": "production"}
)
```

### System Integration Options

The `CelerySystemIntegration` class takes a number of optional parameters:

- `auto_track_tasks`: Set this to `False` to disable automatic tracking of tasks.
- `includes`: A list of task names or patterns to include. If this is set, only tasks that match one of the patterns
  will be tracked.
- `excludes`: A list of task names or patterns to exclude. If this is set, tasks that match one of the patterns will
  not be tracked.
- `record_task_args`: If `True`, the arguments passed to the task will be recorded in the Task Badger task data.
  
    ==Since v1.4.0==

- `heartbeat_interval`: Seconds between automatic task updates while a task is running. See
  [Keeping Long-Running Tasks Fresh](#keeping-long-running-tasks-fresh).

    ==Since v2.4.0==

- `stale_timeout`: The [`stale_timeout`](data_model.md#stale_timeout) to set on tracked tasks.

    ==Since v2.4.0==

Exclusions take precedence over inclusions so if a task name matches both an include and an exclude, it will be
excluded.

## Celery Task Class

To track individual tasks, or if you want access to the `Task` object within the body of the Celery task, you can
use the `taskbadger.celery.Task` class as the base class for your Celery tasks. This can be used with or without
the `CelerySystemIntegration`.

This custom Celery task class tells Task Badger that the task should be tracked irrespective of any configuration
passed to `CelerySystemIntegration` ie. even if the task matches an exclusion rule it will still be tracked if it
is using `taskbadger.celery.Task` as its base.

The task class also provides convenient access to the Task Badger task object within the body of the Celery task.

### Basic Usage

To use the integration simply set the `base` parameter of your Celery task to `taskbadger.celery.Task`:

!!!note inline end ""

    This works the same with the `@celery.shared_task` decorator.

```python
from celery import Celery
from taskbadger.celery import Task

app = Celery("tasks")


@app.task(base=Task)
def my_task():
    pass


result = my_task.delay()
taskbadger_task_id = result.taskbadger_task_id
taskbadger_task = result.get_taskbadger_task()
```

Having made this change, a task will now be automatically created in Task Badger when the celery task is published.
The Task Badger task will also be updated when the task completes.

!!! info

    Note that Task Badger will only track the Celery task if it is run asynchronously. If the task is run
    synchronously via `.apply()`, by calling the function directly, or if [`task_always_eager`][always_eager]{:target="_blank"} has been set,
    the task will not be tracked.

    This also means that the `taskbadger_task_id` attribute of the result as well as the return value
    of `result.get_taskbadger_task()` will be `None` if the task is not being tracked by Task Badger.

[always_eager]: https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_always_eager

### Task Customization

You can pass additional parameters to the Task Badger `Task` class which will be used when creating the task.
This can be done by passing keyword arguments prefixed with `taskbadger_` to the `.appy_async()` function or
to the task decorator.

```python
# using the task decorator

@app.task(base=Task, taskbadger_monitor_id="xyz")
def my_task(arg1, arg2):
    ...


# using individual keyword arguments
my_task.apply_async(
    args=[arg1, arg2],
    taskbadger_name="my task",
    taskbadger_value_max=1000,
    taskbadger_data={"custom": "data"},
)

# using a dictionary
my_task.apply_async(args=[arg1, arg2], taskbadger_kwargs={
    "name": "my task",
    "value_max": 1000,
    "data": {"custom": "data"}
})
```

!!!note "Order of Precedence"

    Values passed via `apply_async` take precedence over values passed in the task decorator.

    In both the decorator and `apply_async`, if individual keyword arguments are used as well as
    the `taskbadger_kwargs` dictionary, the individual arguments will take precedence.


!!!note "Recording task args"

    By default, the arguments passed to the task are not recorded in the Task Badger task data. To record the
    arguments, set the `taskbadger_record_task_args` parameter to `True` in the task decorator or in the `apply_async` call.
    This will override the value set in the `CelerySystemIntegration` if it is being used.

    ==Since v1.4.0==


### Accessing the Task Object

The `taskbadger.celery.Task` class provides access to the Task Badger task object via the `taskbadger_task` property
of the Celery task. The Celery task instance can be accessed within a task function body by creating a
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
    # can also update the `value` property or other task properties.
    task.success(value=len(items))
```

!!!note

    The `taskbadger_task` property will be `None` if the task is not being tracked by Task Badger.
    This could indicate that the Task Badger API has not been [configured](python.md#configure), there was an error
    creating the task, or the task is being run synchronously e.g. via `.apply()` or calling the task
    using `.map` or `.starmap`, `.chunk`.

## Keeping Long-Running Tasks Fresh

==Since v2.4.0==

A task with a [`stale_timeout`](data_model.md#stale_timeout) is marked `stale` if it goes too long
without an update, so a long-running task that doesn't report progress will trip the timeout while it
is perfectly healthy. Setting `heartbeat_interval` (seconds) makes the worker update the task for you
while it runs, instead of having to do it from the task body.

The interval can be set on the system integration, on the task, or per call:

```python
# for all tracked tasks
taskbadger.init(
    token="YOUR_API_KEY",
    systems=[CelerySystemIntegration(heartbeat_interval=60)],
)

# on the task
@app.task(base=Task, taskbadger_heartbeat_interval=60)
def my_task():
    ...

# per call
my_task.apply_async(taskbadger_heartbeat_interval=60)
```

Unless `stale_timeout` is given explicitly it is set to twice the interval, so each of the examples
above creates the task with a `stale_timeout` of 120 seconds. Pass both to control it:

```python
my_task.apply_async(taskbadger_heartbeat_interval=60, taskbadger_stale_timeout=300)
```

As with the other options, values set on the task or on `apply_async` take precedence over the values
set on `CelerySystemIntegration`.

!!! note

    All running tasks are updated from a single background thread per worker process, started the
    first time a task with a heartbeat runs. Updates stop when the task finishes.

## Canvas primitives (map / starmap / chunks)

As of `v1.6.3`, Task Badger now tracks tasks created via Celery canvas primitives: `map`, `starmap`, and `chunks`. Previously these were executed as built-in `celery.map` / `celery.starmap` tasks and were filtered out; TaskBadger now creates task records for the *inner* tasks produced by these primitives.

Behavior summary:

- Canvas primitives produce Task Badger tasks using the inner task's name (so the tracked task has the same name as if the task had been executed individually).
- Each created task includes additional metadata:
  - `canvas_type`: one of `celery.map`, `celery.starmap`, or `celery.chunks`
  - `item_count`: number of inner items produced by the canvas execution (an integer)
  - `celery_task_items`: the arguments passed to the inner task

**Example**

Assume a Celery task:

```python
@app.task(name="myapp.add")
def add(x, y):
    return x + y
```

Running a map:

```python
# This schedules 3 inner tasks
add.map([(1, 2), (2, 3), (3, 4)]).apply_async()
```

Task Badger will create task records for each inner invocation with metadata similar to:

```json
{
  "name": "myapp.add",
  "metadata": {
    "canvas_type": "celery.map",
    "item_count": 3,
    "celery_task_items": [[1, 2], [2, 3], [3, 4]]
  }
}
```

## Subtasks

==Since v2.5.0==

A Celery task published from inside a tracked task is automatically nested under it via the
[`parent`](data_model.md#parent) field, so you can see the work a task spawned.

Tasks nest a single level deep. A task published by a task that is itself a child becomes a sibling
of that child rather than a grandchild.

What gets nested:

- Tasks published from the body of a tracked task via `.delay()` or `.apply_async()`, including when
  Celery runs them eagerly.
- Retries, which are nested under the first attempt.

What does not get nested:

- The next link of a `chain`, and `link` callbacks. These are successors of the task rather than work
  it chose to enqueue.
- Tasks produced by [canvas primitives](#canvas-primitives-map-starmap-chunks) (`map`, `starmap`,
  `chunks`) when they run on a worker. Their Task Badger tasks are created in the worker rather than
  at publish time, so the enclosing task isn't visible there. They do nest when Celery runs eagerly.

!!! note

    Known edge case: if a chain's next link is *also* called directly from the task body, that direct
    call is not nested.

## External ID

The Celery task ID is automatically recorded on the Task Badger task's
[`external_id`](data_model.md#external_id) field, letting you correlate the Task Badger task with the
originating Celery task.

## Opting out

If you want to prevent TaskBadger from tracking a particular execution, set the `taskbadger_track` header (False) when publishing:

```python
add.map([(1, 2), (2, 3)]).apply_async(headers={"taskbadger_track": False})
```
