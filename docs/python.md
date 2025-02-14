# Task Badger Python SDK

On this page, we get you up and running with Task Badger's Python SDK.

## Install

Install the SDK using [pip](https://pip.pypa.io/en/stable/) or your favorite pacakge manager: 

```bash
pip install --upgrade taskbadger
```

## Configure

The SDK must be configured before you can use it to interact with the APIs.

```python
import taskbadger

taskbadger.init(
    organization_slug="my-org",
    project_slug="my-project",
    token="***",
    tags={"environment": "production"},
)
```

Details about the slug configuration parameters can be found [here](basics.md#organization-and-project).

| Name              | Description                                                                                               |
|-------------------|-----------------------------------------------------------------------------------------------------------|
| organization_slug | The organization identifier.                                                                              |
| project_slug      | The project identifier.                                                                                   |
| token             | API authentication token.                                                                                 |
| tags              | Global tags which are added to all tasks.                                                                 |
| systems           | System integrations such as [Celery](python-celery.md)                                                    |
| before_create     | A function that is called before a task is created. See [Before Create Callback](#before-create-callback) |

If you attempt to use the SDK without configuring it you will get an error. To avoid this you can use the
[safe functions](#safe-functions) which will log any errors to the `taskbadger` logger.

!!! tip
    [Tags](data_model.md#tags) provided here will be applied to all tasks created using the SDK. If you need to add tags to individual tasks you can do so using the create and update methods or the `task.add_tag` method. Tags added manually will override the global tags.

## Usage

The SDK provides a [Task](#taskbadger.Task) class which offers a convenient interface to the API.

Tasks are created by calling the `Task.create` method:

```python
from taskbadger import Task, Action, EmailIntegration

# create a new task with custom data and an action definition
task = Task.create(
    "task name",
    data={
        "custom": "data"
    },
    actions=[
        Action(
            trigger="*/10%,success,error",
            integration=EmailIntegration(to="me@example.com")
        )
    ],
    tags={"tenant": "acme"}
)
```

Alternatively a task may be retrieved via the tasks ID:

```python
from taskbadger import Task

task = Task.get(task_id)
```

The task object provides methods for updating the properties of a task, adding custom data
and adding actions.

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

## Python Reference

::: taskbadger.Task

## Low level functions
In addition to the `taskbadger.Task` class. There are also a number of functions that provide lower level
access to the API:

::: taskbadger.get_task

::: taskbadger.create_task

::: taskbadger.update_task

## Safe functions

For instances where you prefer not to handle errors you can use the following function which will handle
all errors and log them to the `taskbadger` logger.

These can also be used safely in instances where the API has not been configured via `taskbadger.init`.

::: taskbadger.create_task_safe

::: taskbadger.update_task_safe
