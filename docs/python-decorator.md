# Python Function Decorator

In addition to the `taskbadger.Task` class and utility functions, there is also a
function decorator that can be used to automatically create a task when a function is called.

```python
from taskbadger import track

@track("my task")
def my_function():
    pass
```

Using the decorator will create a task with the name provided and automatically update the task
status to `success` when the function completes or `error` if an exception is raised.

The decorator also applies the `taskbadger.Session` context manager to the function.
See [connection management](python.md#connection-management).

When the function raises, the exception is recorded on the task data along with any context from the
configured [context providers](python.md#error-context-providers).

## Nested tasks

==Since v2.5.0==

Tasks tracked by another integration while a decorated function is running are nested under its task
via the [`parent`](data_model.md#parent) field. That means other `@track` decorated functions called
from the body, as well as [Celery](python-celery.md#subtasks) and
[Procrastinate](python-procrastinate.md#subtasks) tasks enqueued from it. A bare `Task.create` in the
function body is not nested unless you pass `parent` yourself.

Each integration carves out some exceptions — Celery, for instance, doesn't nest chain successors,
`link` callbacks, or canvas primitives running on a worker. The [Celery](python-celery.md#subtasks) and
[Procrastinate](python-procrastinate.md#subtasks) pages list what does and doesn't get nested.

Tasks nest a single level deep, so anything created by a decorated function that is itself a child
becomes a sibling of that child rather than a grandchild. Passing `parent` to the decorator explicitly
overrides the automatic nesting.

## API Docs

::: taskbadger.track
