---
title: API Endpoints
---

All tasks (and related data) is associated with a single project. The base
task URL is:

    /api/{organization}/{project}/tasks


| Action              | Endpoint                                                                                                                      |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------|
| List tasks          | `GET /api/{org}/{project}/tasks`                                                                                              |
| Create task         | `POST /api/{org}/{project}/tasks`                                                                                             |
| Get task details    | `GET /api/{org}/{project}/tasks/{task_id}`                                                                                    |
| Update task         | `PATCH /api/{org}/{project}/tasks/{task_id}`                                                                                  |
| Cancel task         | `DELETE /api/{org}/{project}/tasks/{task_id}`                                                                                 |
| List task actions   | `GET /api/{org}/{project}/tasks/{task_id}/actions/`                                                                           |
| Add task action     | `POST /api/{org}/{project}/tasks/{task_id}/actions/`<br/>(alternately POST to 'update task' endpoint with {"actions": [...]}) |
| Update task action  | `PATCH /api/{org}/{project}/tasks/{task_id}/actions/{action_id}/`                                                             |
| Cancel task action  | `DELETE /api/{org}/{project}/tasks/{task_id}/actions/{action_id}/`                                                            |


Full details of the API endpoints can be viewed at [https://taskbadger.net/api/docs/](https://taskbadger.net/api/docs/){:target="_blank"}
