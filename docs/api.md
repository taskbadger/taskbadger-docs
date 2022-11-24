---
title: API Endpoints
---

# Tasks

All tasks (and related data) is associated with a single project. The base
task URL is:

    /api/{organization}/{project}/tasks


| Action              | Endpoint                                                                                                                     |
|---------------------|------------------------------------------------------------------------------------------------------------------------------|
| List tasks          | `GET /api/{org}/{project}/tasks`                                                                                             |
| Create task         | `POST /api/{org}/{project}/tasks`                                                                                            |
| Get task details    | `GET /api/{org}/{project}/tasks/{task_id}`                                                                                   |
| Update task         | `POST /api/{org}/{project}/tasks/{task_id}`                                                                                  |
| Cancel task         | `DELETE /api/{org}/{project}/tasks/{task_id}`                                                                                |
| List task actions   | `GET /api/{org}/{project}/tasks/{task_id}/actions`                                                                           |
| Add task action     | `POST /api/{org}/{project}/tasks/{task_id}/actions`<br/>(alternately POST to 'update task' endpoint with {"actions": [...]}) |
| Update task action  | `POST /api/{org}/{project}/tasks/{task_id}/actions/{action_id}`                                                              |
| Cancel task action  | `DELETE /api/{org}/{project}/tasks/{task_id}/actions/{action_id}`                                                            |



# Actions

Actions are at the core of Task Badger's secret sauce. They allow you to send notifications, perform callouts,
and more based on task events.

Every action specifies an integration e.g. `email`, and a trigger definition which is
like a crontab expression, but for tasks. For example, `*/25%,success` means, "execute
this action when the task value passes 25%, 50%, 75%, 100% and when the task status
is set to `success`".

A task may have multiple actions, each with their own integration and trigger definition.

## Edge cases

If a task value or status skips past multiple trigger points, only the last matching trigger will be
executed.

For example, an action configured with `20,40,80` whose value goes from `0` directly to `90` will
skip over the `20` and `40` events and only fire the `80` event. This also applies to task
status triggers.
