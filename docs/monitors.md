---
title: Cron Monitors
---
# Scheduled Task Monitors

A common need in task monitoring is being notified if a scheduled task fails or doesn't run.
It is easy to determine if tasks are successful using the task itself but detecting if a task fails or
does not run at all requires a separate system.

This is where Task Badger Monitors can help.

By registering a task with Task Badger you can be sure that if the task fails or takes too long
you will get notified.

But what if the task never runs at all and never gets registered with Task Badger? We've got you
covered there too. By telling Task Badger when you expect the task to run we can check and make
sure that it does actually run when it's supposed to.

## Creating a monitor

Monitors are created via the Task Badger web UI. When creating a monitor you will need to chose
between two types: "interval" and "cron".

## Interval Monitors

Use an interval monitor when your tasks are scheduled in a chain (one after the other) and not based
on real time.

For example, a task that runs every 5 minutes where each task is scheduled after the previous task
starts / ends.

[//]: # (what about drift - make check-ins start after last end)

## Cron Monitors

Use a cron monitor when you need more advanced scheduling or when your tasks are executed based on
real time, for example, once per hour, on the hour.

Cron monitor require writing cron schedule expressions. Cron expressions are split up in 5 fields
as follows:

```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
```

Here are some examples:

| Expression    | Description                     |
|---------------|---------------------------------|
| `1 0 * * *`   | Daily at 1 minute past midnight |
| `0 */2 * * *` | Every 2nd hour                  |
| `45 23 * * 6` | 23:45 every Saturday (day 6)    |

For a more detailed explanation see [Wikipedia](https://en.wikipedia.org/wiki/Cron#Overview).

[//]: # (grace period)
[//]: # (max runtime)


## Set Up

Once you have created a monitor you need to configure your tasks to notify Task Badger when they
run.

### Using the CLI

The CLI provides an easy way to monitor your tasks. To associate a task with a monitor simply
provide the monitor ID:


```bash
$ taskbadger run "run script" --monitor-id=XYZ -- path/to/script.sh
```

### Using the API

=== "Python"

    ```python
    from taskbadger import Task, StatusEnum
    task = Task.create(name"my-task", status=StatsuEnum.processing, monitor_id="XYZ")
    try:
        # Execute your task here...
    except Exception as e:
        task.error({
            "exception": str(e)
        })
    else:
        task.update(status=StatusEnum.success)
    ```

=== "Shell"

    Using the API directly you can pass the monitor ID vai the `X-TASKBADGER-MONITOR`
    header. The monitor ID only needs to be included in the request to create the task.

    ``` { .shell hl_lines="3" }
    curl -X POST "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "X-TASKBADGER-MONITOR: %{MONITOR_ID}" \
      -H "Content-Type: application/json" \
      -d '{"name": "demo task", "status": "processing"}'
    # Response { "id": "128aoa98e0fiq238" ...}

    # Execute your scheduled task here...

    curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/128aoa98e0fiq238/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"status": "success"}'    
    ```
