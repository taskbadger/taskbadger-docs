---
title: Quick Start
---
# Get the Badger working!

Let's discover **Task Badger in less than 5 minutes**.

## Setup

In order to use the API you will need the follwing details:

* Organization slug
    * You can get this by going to 'My Organization'  
* Project slug
    * Go to the 'Projects' page. The slug for each project is listed. 
* API Key
    * Create one on your Profile page

=== "Python"

    ```python
    import taskbadger

    taskbadger.init(
        organization_slug="my-org",
        project_slug="my-project",
        token="***"
    )
    ```

=== "Shell"

    ```shell
    export ORG="organization slug"
    export PROJECT="project slug"
    export API_KEY="api key"
    ```

## Creating a task

Creating a task is very simple. Make a POST request to the API with the task
data.

=== "Python"

    ```python
    > task = Task.create("task name")
    > task.id
    "128aoa98e0fiq238"
    ```

=== "Shell"

    ```shell
    $ curl -X POST "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"name": "demo task"}'
    ```

    The response will include the task ID which is needed for updating the task.
    
    ```json title="Response"
    {
      "id": "${TASK_ID}",
      "organization":"{organization}",
      "project": "{project}",
      "name":"demo task",
      "status":"pending",
      "value":null,
      "value_max":null,
      "value_percent":null,
      "data":null,
      "created":"2022-09-22T06:53:40.683555Z",
      "updated":"2022-09-22T06:53:40.683555Z"
    }
    ```

The task will now be listed in the task list: `https://taskbadger.net/a/${ORG}/tasks/`.

## Update task progress

Here we update the task `status` and `value`. By default, a task's value can range from
0 to 100.

=== "Python"

    ```python
    from taskbadger import StatusEnum
    task.update(status=StatusEnum.processing, value=5)
    ```

=== "Shell"
    
    ```shell
    $ curl -X POST "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/${TASK_ID}/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"status": "processing", "value": 5}'
    ```

## Add an action to the task

Here we update create a new action for the task so that we get notified when the task completes.

=== "Python"

    ```python
    from taskbadger import Action, EmailIntegration
    task.add_actions([
        Action(
            "*/10%,success,error",
            integration=EmailIntegration(to="me@example.com")
        )
    ]
    ```

=== "Shell"
    
    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/${TASK_ID}/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"actions":[{"integration":"email","trigger":"success,error","config":{"to":"me@example.com"}}]}'
    ```

## Mark the task complete

When the task is complete update the status to either `success` or `error`.
The value may also be updated to 100.

=== "Python"
  
    ```python
    task.update(status=StatusEnum.success, value=100)
    ```

=== "Shell"

    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/${TASK_ID}/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"status": "success", "value": 100}'
    ```
Also check your email to see if you got the notification.
