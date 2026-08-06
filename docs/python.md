# Task Badger Python SDK

On this page, we get you up and running with Task Badger's Python SDK.

## Install

Install the SDK using [uv](https://docs.astral.sh/uv/) or your favorite package manager:

```bash
uv pip install taskbadger
```

## Configure

The SDK must be configured before you can use it to interact with the APIs.

```python
import taskbadger

taskbadger.init(
    token="YOUR_API_KEY",
    tags={"environment": "production"},
)
```

When using a Project API Key, the organization and project are detected
automatically from the key. You can find your API key on the project settings
page in the [Task Badger dashboard](https://taskbadger.net).

| Name              | Description                                                                                               |
|-------------------|-----------------------------------------------------------------------------------------------------------|
| token             | Project API key. The organization and project are extracted from the key automatically.                    |
| tags              | Global tags which are added to all tasks.                                                                 |
| systems           | System integrations such as [Celery](python-celery.md)                                                    |
| before_create     | A function that is called before a task is created. See [Before Create Callback](#before-create-callback) |
| context_providers | Providers that attach extra data to a task when it errors. See [Error Context Providers](#error-context-providers) |
| organization_slug | The organization identifier. Only required for legacy API keys.                                           |
| project_slug      | The project identifier. Only required for legacy API keys.                                                |

If you attempt to use the SDK without configuring it you will get an error. To avoid this you can use the
[safe functions](#safe-functions) which will log any errors to the `taskbadger` logger.

!!! tip
    [Tags](data_model.md#tags) provided here will be applied to all tasks created using the SDK. If you need to add tags to individual tasks you can do so using the create and update methods or the `task.add_tag` method. Tags added manually will override the global tags.

## Usage

The SDK provides a [Task](#taskbadger.Task) class which offers a convenient interface to the API.

Tasks are created by calling the `Task.create` method:

```python
from taskbadger import Task

# create a new task with custom data and tags
task = Task.create(
    "task name",
    data={
        "custom": "data"
    },
    tags={"tenant": "acme"}
)
```

Alternatively a task may be retrieved via the tasks ID:

```python
from taskbadger import Task

task = Task.get(task_id)
```

The task object provides methods for updating the properties of a task and adding custom data.

### Listing tasks

`list_tasks` returns a [`TaskList`](#taskbadger.TaskList), a single page of tasks that you can iterate
over directly. The tasks it yields are ordinary `Task` objects, so they can be updated in place:

```python
import taskbadger
from taskbadger import StatusEnum

for task in taskbadger.list_tasks(page_size=50):
    if task.status == StatusEnum.PENDING:
        task.canceled()
```

The `next_` and `previous` attributes hold the URL of the adjacent page, or are unset if there isn't
one. To fetch the next page, pass its `cursor` query parameter back to `list_tasks`:

```python
from urllib.parse import parse_qs, urlparse

page = taskbadger.list_tasks(page_size=100)
while True:
    for task in page:
        ...
    if not page.next_:
        break
    cursor = parse_qs(urlparse(page.next_).query)["cursor"][0]
    page = taskbadger.list_tasks(page_size=100, cursor=cursor)
```

!!! note "Changed in v2.5.1"

    `list_tasks` previously returned the generated `PaginatedTaskList` whose `results` were
    `taskbadger.internal.models.Task` objects, without the SDK's `update()` / `safe_update()` methods.
    It now returns a `TaskList` of `taskbadger.Task` objects.

    A `TaskList` also has a length, so an empty page is falsy where `PaginatedTaskList` was always
    truthy. If you have code like `if taskbadger.list_tasks(...):`, note that it now tests whether the
    page has any tasks in it.

### Parent and child tasks

==Since v2.5.0==

A task can be nested under another task by passing the parent's ID as the
[`parent`](data_model.md#parent) field:

```python
from taskbadger import Task

parent = Task.create("import")
child = Task.create("import.chunk", parent=parent.id)
```

Tasks nest a single level deep, so `parent` must be the ID of a task that is not itself a child.
A task's parent can not be changed once it has been set.

Use `list_tasks` to fetch the children of a task:

```python
import taskbadger

for child in taskbadger.list_tasks(parent=parent.id):
    print(child.name, child.status)
```

`Task.create` and `create_task` only nest a task when you pass `parent` explicitly. The
[function decorator](python-decorator.md#nested-tasks), [Celery](python-celery.md#subtasks) and
[Procrastinate](python-procrastinate.md#subtasks) integrations do it for you: a task enqueued while
another tracked task is running is nested under it automatically.

### Connection management

The SDK will open a new connection for each request and close it when the request is complete. For instances
where you wish to make multiple requests you can use the `taskbadger.Session` context manager:

```python
from taskbadger import Session

with Session() as session:
    task = Task.create("my task")
    task.update(status="success")
```

If you are using the [function decorator](python-decorator.md) or the [Celery integration](python-celery.md), 
session management is handled automatically within the body of the function or Celery task.

### Scope

The SDK provides the `taskbadger.current_scope` context manager which can be used to set custom data and modify tags for the duration of the context. The content of the scope will be merged with any custom task data passed directly to any of the other API methods.

```python
import socket
import taskbadger

with taskbadger.current_scope() as scope:
    scope["hostname"] = socket.gethostname()
    scope.tag({"tenant": "acme"})
```

A common use case for this is to add request scoped context in frameworks like Django or Flask using a custom
middleware. Here's an example for Django:

```python
import taskbadger

def taskbadger_scope_middleware(get_response):
    def middleware(request):
        with taskbadger.current_scope() as scope:
            scope["user"] = request.user.username
            scope.tag({"tenant": request.tenant.slug})
            return get_response(request)

    return middleware
```

!!!note

    The data passed directly to the API will take precedence over the data in the current scope. If the same
    key is present in the current scope as well as the data passed in directly, the value in the data passed
    directly will be used. The same applies to tags.

## Before Create Callback

The `before_create` parameter in the `taskbadger.init` function allows you to define a function that will be called before a task is created. This function will be passed the task data as a dictionary and should return the modified task data.

```python
def before_create(task_data: dict) -> dict:
    data = task_data.setdefault("data", {})
    data["custom"] = "data"
    
    tags = task_data.setdefault("tags", {})
    tags["tenant"] = "acme"
    
    return task_data
```

==Since v1.5.0==

## Error Context Providers

==Since v2.5.0==

Context providers attach extra data to a task when it errors, for example a link back to the system
that reported the exception. They are consulted whenever a tracked task fails — via the
[function decorator](python-decorator.md), the [Celery](python-celery.md) or
[Procrastinate](python-procrastinate.md) integrations, or `Task.error(exception=...)` — and whatever
a provider returns is stored on the task [`data`](data_model.md#data) under the provider's identifier.

Providers are registered with `taskbadger.init`:

```python
import taskbadger
from taskbadger.context_providers.sentry import SentryContextProvider

taskbadger.init(
    token="YOUR_API_KEY",
    context_providers=[SentryContextProvider(organization_slug="acme")],
)
```

A provider that raises is logged to the `taskbadger` logger and skipped, so it can never break the
task update.

### Sentry

`SentryContextProvider` links a failed task to the Sentry issue for the same exception. It requires
the `sentry-sdk` package, available via the `sentry` extra:

```bash
uv add 'taskbadger[sentry]'
# or: pip install 'taskbadger[sentry]'
```

```python
import taskbadger
from taskbadger.context_providers.sentry import SentryContextProvider

taskbadger.init(
    token="YOUR_API_KEY",
    context_providers=[SentryContextProvider(organization_slug="acme")],
)
```

Failed tasks then carry the Sentry event ID in their data, plus a link to the issue when
`organization_slug` is given:

```json
{
  "exception": "bad input",
  "sentry": {
    "event_id": "5f8a...",
    "url": "https://sentry.io/organizations/acme/issues/?query=5f8a..."
  }
}
```

Pass `base_url` if you are running a self-hosted Sentry.

!!! note

    The provider does not report the exception to Sentry itself. It assumes your application already
    does that (e.g. via a framework integration) and reads back the event ID, which avoids reporting
    the same exception twice. If the exception never reaches Sentry, no context is added.

### Custom providers

To attach context from another system, subclass `ContextProvider`, set an `identifier` and implement
`capture_error_context`:

```python
from taskbadger.context_providers import ContextProvider


class RequestIdProvider(ContextProvider):
    identifier = "request"

    def capture_error_context(self, exception, snapshot=None):
        return {"id": get_current_request_id()}
```

Providers that read back state captured by another system, rather than capturing it themselves,
should also implement `snapshot`. It is called when a tracked task starts and its return value is
passed back as `snapshot`, so the provider can tell a fresh capture from a stale one left over from
something unrelated.

## Python Reference

::: taskbadger.Task

## Low level functions
In addition to the `taskbadger.Task` class. There are also a number of functions that provide lower level
access to the API:

::: taskbadger.get_task

::: taskbadger.create_task

::: taskbadger.update_task

::: taskbadger.list_tasks

::: taskbadger.TaskList

## Context Provider Reference

::: taskbadger.context_providers

::: taskbadger.context_providers.sentry.SentryContextProvider

## Safe functions

For instances where you prefer not to handle errors you can use the following function which will handle
all errors and log them to the `taskbadger` logger.

These can also be used safely in instances where the API has not been configured via `taskbadger.init`.

::: taskbadger.create_task_safe

::: taskbadger.update_task_safe
