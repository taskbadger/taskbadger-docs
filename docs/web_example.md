---
title: Example Walkthrough
---

Here we'll see how to use Task Badger in a web setting to create a task during a request
and then updated it as the task is processed on the backend.

In the following example we'll be using Django and Celery.

!!! tip

    If using the Task Badger task for local progress tracking seems a bit heavy for your use case, you could
    use [celery-progress](https://pypi.org/project/celery-progress/){:target="_blank"} for local tracking and
    maintain the Task Badger task purerly for remote tracking, metrics, alerts, integrations etc.

## Option 1: Use the Core API

### 1. Create the task in a view

```python title="views.py"
from django.conf import settings
from taskbadger import StatusEnum, Task
from apps.export.tasks import export_user_data

NOTIFY_EMAIL = settings.ADMINS[0][1]


@require_POST
def export_data(request):
    task = Task.create(
        "data export",
        data={"user_id": request.user.id},
        actions=[Action("error,stale", integration=EmailIntegration(to=NOTIFY_EMAIL))],
        stale_timeout=5,  # minutes
    )

    export_user_data.delay(task_id=task.id, user_id=request.user.id)
    return JsonResponse({"task_id": task.id})
```

In addition to creating the task, we've also added an action so that we will get notified if the task
fails or does not complete.

### 2. Update the task 

```python title="tasks.py"
from celery.app import shared_task
from taskbadger import StatusEnum, Task

@shared_task
def export_user_data(task_id, user_id):
    task = Task.get(task_id)
    task.update(status=StatusEnum.PROCESSING)

    try:
        compile_export(task, user_id)  # this also updates the task progress
    except Exception as e:
        task.error(data={
            "error": str(e)
        })
        raise
    
    task.success(100)
```

### 3. Expose the task status for the UI

```python title="views.py"
@require_GET
def poll_task_status(request, task_id):
    task = Task.get(task_id)
    
    return JsonResponse({
        "status": task.status,
        "value": task.value,
        "value_percent": task.value_percent
    })
```


## Option 2: Use the Celery integration

Use the Task Badger Celery Task class as the base class for your Celery task:

```python title="tasks.py"
from celery.app import shared_task
from taskbadger.celery import Task

@shared_task(bind=True, base=Task, taskbadger_kwargs={
    "actions": [Action("error,stale", integration=EmailIntegration(to=settings.ADMINS[0][1]))],
    "stale_timeout": 5
})
def export_user_data(self, user_id):
    task = self.taskbadger_task

    try:
        compile_export(task, user_id)  # this also updates the task progress
    except Exception as e:
        task.error(data={
            "error": str(e)
        })
        raise
    
    task.success(100)
```

In the view we can get the Task Badger task ID from the Celery task result:

```python title="views.py"
from apps.export.tasks import export_user_data


@require_POST
def export_data(request):
    task = export_user_data.delay(user_id=request.user.id, taskbadger_data={"user_id": request.user.id})
    tb_task_id = task.info.get("taskbadger_task_id")
    return JsonResponse({"task_id": tb_task_id})


@require_GET
def poll_task_status(request, task_id):
    # same as above
```
