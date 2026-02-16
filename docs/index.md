# Task Badger Documentation

Task Badger is a monitoring and observability platform for background jobs and async tasks. It integrates with task processing systems like Celery to give you visibility into task progress, performance, and failures.

![Task Badger](assets/visualization.png)

## Get Started

Install the Python SDK:

```bash
uv pip install taskbadger
```

Initialize with your [Project API Key](https://taskbadger.net):

```python
import taskbadger

taskbadger.init(token="YOUR_API_KEY")
```

Create and track a task:

```python
from taskbadger import Task, StatusEnum

task = Task.create("my task")
task.update(status=StatusEnum.PROCESSING, value=50)
task.update(status=StatusEnum.SUCCESS, value=100)
```

Or monitor Celery tasks automatically with the [Celery integration](python-celery.md):

```python
from taskbadger.systems import CelerySystemIntegration

taskbadger.init(
    token="YOUR_API_KEY",
    systems=[CelerySystemIntegration()]
)
```

Or track any shell command with the [CLI](cli.md):

```bash
taskbadger run "my task" -- ./script.sh
```

## Key Features

- **Task tracking** — monitor status, progress, and metadata for any background job
- **Celery integration** — automatic tracking of all Celery tasks with zero code changes
- **Actions and triggers** — get notified via email, webhook, or other integrations on task events
- **CLI** — monitor shell commands without writing code

## Learn More

- [Quick Start](quick.md) — full setup walkthrough
- [Python SDK](python.md) — SDK reference
- [CLI](cli.md) — command line usage
- [Data Model](data_model.md) — task states, actions, and triggers
- [API Endpoints](api.md) — REST API reference
