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

## API Docs

::: taskbadger.track