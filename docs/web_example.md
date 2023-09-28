---
title: Example Walkthrough
---

Here we'll see how to use Task Badger in a web setting to create a task during a request
and then updated it as the task is processed on the backend.

In the following example we'll be using Django and Celery.

## 1. Create the task in a view

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
        stale_timeout=60,  # seconds
    )

    export_user_data.delay(task_id=task.id, user_id=request.user.id)
    return JsonResponse({"task_id": task.id})
```

In addition to creating the task, we've also added an action so that we will get notified if the task
fails or does not complete.

## 2. Update the task 

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

## 3. Expose the task status for the UI

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
