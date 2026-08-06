# Procrastinate Integration

==Since v2.1.0==

The Procrastinate integration lets you automatically create and update Task Badger tasks from
[Procrastinate](https://procrastinate.readthedocs.io/){:target="_blank"} jobs. It tracks the full
lifecycle of a job — `pending` when the job is deferred, `processing` when the worker starts it, and
`success` or `error` when it finishes.

Install the optional extra to pull in Procrastinate:

```bash
uv add 'taskbadger[procrastinate]'
# or: pip install 'taskbadger[procrastinate]'
```

There are two ways to use the integration:

1. Use the `ProcrastinateSystemIntegration` to automatically track all tasks on a Procrastinate `App`.
2. Use the `@track` decorator on individual tasks you wish to track.

You can use both at the same time. The `@track` decorator is also useful when you want to access the
Task Badger task object within the body of a job.

## Procrastinate System Integration

To track every task on a Procrastinate `App`, register the `ProcrastinateSystemIntegration` when
initializing Task Badger:

```python
import taskbadger
from taskbadger.systems.procrastinate import ProcrastinateSystemIntegration

taskbadger.init(
    token="YOUR_API_KEY",
    systems=[ProcrastinateSystemIntegration(app=my_procrastinate_app)],
    tags={"environment": "production"},
)
```

### System Integration Options

The `ProcrastinateSystemIntegration` class takes the following parameters:

- `app`: The `procrastinate.App` instance to instrument. **Required.**
- `auto_track_tasks`: Set this to `False` to disable automatic tracking of tasks. Tasks decorated with
  `@track` will still be tracked.
- `includes`: A list of task names or regex patterns to include. If this is set, only tasks that match
  one of the patterns will be tracked.
- `excludes`: A list of task names or regex patterns to exclude. If this is set, tasks that match one of
  the patterns will not be tracked.
- `record_task_args`: If `True`, the job's keyword arguments will be recorded in the Task Badger task
  data under `procrastinate_task_kwargs`.
- `heartbeat_interval`: Seconds between automatic task updates while a task is running. See
  [Keeping Long-Running Tasks Fresh](#keeping-long-running-tasks-fresh). ==Since v2.4.0==
- `stale_timeout`: The [`stale_timeout`](data_model.md#stale_timeout) to set on tracked tasks.
  ==Since v2.4.0==

Patterns are matched against the full task name using `re.fullmatch`. Exclusions take precedence over
inclusions, so if a task name matches both an include and an exclude, it will be excluded.

Procrastinate's built-in housekeeping tasks (those named `builtin:...` or `procrastinate.*`) are never
auto-tracked.

```python
taskbadger.init(
    token="YOUR_API_KEY",
    systems=[ProcrastinateSystemIntegration(
        app=app,
        includes=[r"myapp\..*"],
        excludes=[r"myapp\.cleanup\..*"],
        record_task_args=True,
    )],
)
```

!!! info

    Construct the integration **after** all tasks and blueprints have been registered on the `App`.
    Tasks added via `app.add_tasks_from(blueprint)` after the integration is constructed are not
    auto-instrumented — apply `@track` to those tasks explicitly.

## The `track` Decorator

To track individual tasks, or if you want access to the Task Badger task object within the body of a
job, apply the `@track` decorator **outside** (above) the `@app.task` decorator:

```python
import procrastinate
from taskbadger.procrastinate import track

app = procrastinate.App(connector=...)


@track
@app.task(queue="default")
async def add(a, b):
    return a + b
```

With this change a Task Badger task is created in the `pending` state when the job is deferred, and it
is updated to `processing` and then `success` or `error` as the worker runs it.

Tasks decorated with `@track` are always tracked, irrespective of the `includes` / `excludes` rules on
the `ProcrastinateSystemIntegration`.

### Task Customization

The `@track` decorator accepts the following optional keyword arguments, applied when the Task Badger
task is created:

- `name`: The Task Badger task name. Defaults to the Procrastinate task's name.
- `value_max`: The maximum value for the task.
- `tags`: A dictionary of tags applied to the task.
- `data`: A dictionary of initial data merged into the task.
- `record_task_args`: If `True`, the job's keyword arguments are recorded under
  `data["procrastinate_task_kwargs"]`. Defaults to inheriting the value from the
  `ProcrastinateSystemIntegration` if one is configured, otherwise `False`.
- `heartbeat_interval`: Seconds between automatic task updates while the task is running. See
  [Keeping Long-Running Tasks Fresh](#keeping-long-running-tasks-fresh). ==Since v2.4.0==
- `stale_timeout`: The [`stale_timeout`](data_model.md#stale_timeout) to set on the task.
  ==Since v2.4.0==

`record_task_args`, `heartbeat_interval` and `stale_timeout` are inherited from the
`ProcrastinateSystemIntegration` when they are not set on the decorator.

```python
@track(name="report", value_max=100, tags={"env": "prod"}, record_task_args=True)
@app.task
async def report(rows):
    ...
```

## Accessing the Task Object

Use `current_task()` to get the Task Badger task for the currently-running job. This is useful for
updating progress or data from within the job body:

```python
from taskbadger.procrastinate import track, current_task


@track
@app.task
async def report(rows):
    tb = current_task()
    for i, row in enumerate(rows):
        await process(row)
        if i % 10 == 0:
            tb.update(value=i, value_max=len(rows))
```

!!! note

    `current_task()` returns `None` outside of a tracked job, if Task Badger has not been
    [configured](python.md#configure), or if the task could not be fetched.

## Keeping Long-Running Tasks Fresh

==Since v2.4.0==

A task with a [`stale_timeout`](data_model.md#stale_timeout) is marked `stale` if it goes too long
without an update, so a long-running task that doesn't report progress will trip the timeout while it
is perfectly healthy. Setting `heartbeat_interval` (seconds) makes the worker update the task for you
while it runs, instead of having to do it from the job body.

The interval can be set on the task or on the system integration:

```python
# on the task
@track(heartbeat_interval=60)
@app.task
async def slow_job():
    ...


# for all tracked tasks
taskbadger.init(
    token="YOUR_API_KEY",
    systems=[ProcrastinateSystemIntegration(app=app, heartbeat_interval=60)],
)
```

Unless `stale_timeout` is given explicitly it is set to twice the interval, so both of the examples
above create tasks with a `stale_timeout` of 120 seconds. Pass both to control it:

```python
@track(heartbeat_interval=60, stale_timeout=300)
@app.task
async def slow_job():
    ...
```

!!! note

    All running tasks are updated from a single background thread per worker process, started the
    first time a task with a heartbeat runs. Updates stop when the task finishes.

## Periodic Tasks

Periodic tasks scheduled with `@app.periodic` are tracked as well. Each periodic deferral creates a new
Task Badger task, so you can monitor the history and health of your scheduled jobs.

## Queue Field

The name of the Procrastinate queue a task is deferred to is automatically recorded on the Task Badger
task's [`queue`](data_model.md#queue) field.

## Subtasks

==Since v2.5.0==

A job deferred from inside a tracked task is automatically nested under it via the
[`parent`](data_model.md#parent) field, so you can see the work a job spawned.

Tasks nest a single level deep, so a job deferred by a task that is itself a child becomes a sibling
of that child rather than a grandchild.

Nesting relies on the same wrapping as the rest of the integration, so the deferrals listed under
[Known Limitations](#known-limitations) are neither tracked nor nested.

## External ID

The Procrastinate job ID is automatically recorded on the Task Badger task's
[`external_id`](data_model.md#external_id) field, letting you correlate the Task Badger task with the
originating Procrastinate job.

## Known Limitations

Procrastinate has no signals or middleware system, so the integration works by wrapping the task
function and the `defer` methods. This leads to a few cases that are not tracked:

- **`task.configure(...).defer(...)` is not tracked.** `configure()` returns a separate `JobDeferrer`
  whose methods bypass the wrapper. Use `task.defer(...)` directly for tracked deferrals. Jobs deferred
  via `configure().defer()` will still run normally, they just won't appear in Task Badger.
- **`task.batch_defer*` is not tracked**, for the same reason.
- **Tasks added via `app.add_tasks_from(blueprint)` after the `ProcrastinateSystemIntegration` is
  constructed are not auto-instrumented.** Construct the integration after all blueprints are
  registered, or apply `@track` to those tasks explicitly.

Cancelled, aborted, and retried jobs surface as `error` in Task Badger.
