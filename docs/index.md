---
title: Quick Start
---
# Get the Badger working!

Let's discover **Task Badger in less than 5 minutes**.

## Setup

In order to use the API you will need the following details:

* Organization slug
    * You can get this by going to 'My Organization'  
* Project slug
    * Go to the 'Projects' page. The slug for each project is listed. 
* API Key
    * Create one on your Profile page


## Monitor a task from the command line

The Task Badger CLI allows you to run commands from the shell and have them monitored
by Task Badger. The task status will get updated once the command completes.

### Install and configure the CLI

```bash
$ python3 -m pip install taskbadger

$ taskbadger configure

Organization slug: my-org 
Project slug: project-x 
API Key: XYZ.ABC

Config written to ~/.config/taskbadger/confi
```

### Use the CLI to run and monitor the command

```shell
$ taskbadger run "demo task" \
  --action "error email to:me@test.com" \
  -- path/to/script.sh

Task created: https://taskbadger.net/public/tasks/xyz/
```

If the command completes with a non-zero exit code the task status will be set to `error`
and an email will be sent to `me@test.com`.

See more about the [CLI](cli.md).

## Use the API directly



=== "Python"

    Install the `taskbadger` Python library:

    ```shell
    $ python3 -m pip install taskbadger
    ```

    Configure the API client:

    ```python
    import taskbadger

    taskbadger.init(
        organization_slug="my-org",
        project_slug="my-project",
        token="***"
    )
    ```

=== "Shell"

    Export the configuration parameters:

    ```shell
    export ORG="my-org"
    export PROJECT="my-project"
    export API_KEY="***"
    ```

### Creating a task

Creating a task is very simple. Make a POST request to the API with the task
data.

=== "Python"

    ```python
    > task = Task.create("task name", stale_timeout=10)
    > task.id
    "128aoa98e0fiq238"
    ```

=== "Shell"

    ```shell
    $ curl -X POST "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"name": "demo task", "stale_timeout": 10}'
    ```

    The response will include the task ID which is needed for updating the task.
    
    ```json title="Response"
    {
      "id": "{task_id}",
      "organization": "my-org",
      "project": "my-project",
      "name": "demo task",
      "status": "pending",
      "value": null,
      "value_max": null,
      "value_percent": null,
      "data": null,
      "max_runtime": null,
      "stale_timeout": 10,
      "start_time": null,
      "end_time": null,
      "created": "2022-09-22T06:53:40.683555Z",
      "updated": "2022-09-22T06:53:40.683555Z"
      "url": "https://taskbadger.net/a/{example_org/tasks/{task_id}/",
      "public_url": "https://taskbadger.net/public/tasks/{task_id}/"
    }
    ```

The task will now be listed in the task list: `https://taskbadger.net/a/${ORG}/tasks/`.

### Update task progress

Here we update the task `status` and `value`. By default, a task's value can range from
0 to 100.

=== "Python"

    ```python
    from taskbadger import StatusEnum
    task.update(status=StatusEnum.PROCESSING, value=5)
    ```

=== "Shell"

    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/${TASK_ID}/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"status": "processing", "value": 5}'
    ```

### Add an action to the task

Here we update create a new action for the task so that we get notified when the task completes.

=== "Python"

    ```python
    from taskbadger import Action, EmailIntegration
    task.add_actions([
        Action(
            "*/10%,success,error",
            integration=EmailIntegration(to="me@example.com")
        )
    ])
    ```

=== "Shell"
    
    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/${TASK_ID}/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"actions":[{"integration":"email","trigger":"success,error","config":{"to":"me@example.com"}}]}'
    ```

Read more about [actions](data_model.md#task-actions).

### Mark the task complete

When the task is complete update the status to either `success` or `error`.
The value may also be updated to 100.

=== "Python"
  
    ```python
    task.update(status=StatusEnum.SUCCESS, value=100)
    ```

=== "Shell"

    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/${TASK_ID}/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"status": "success", "value": 100}'
    ```
Also check your email to see if you got the notification.

## A real example

Take a look at how to apply this to a real [example](web_example.md).
