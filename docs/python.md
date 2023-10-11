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
    token="***"
)
```

Details about these configuration parameters can be found [here](basics.md#organization-and-project)

If you attempt to use the SDK without configuring it you will get an error. To avoid this you can use the
[safe functions](#safe-functions) which will log any errors to the `taskbadger` logger.

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
    ]
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
