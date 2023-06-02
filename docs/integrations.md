---
title: Integrations
---

# Integrations

Task Badger integrations are what power the actions. When an action is triggered it causes
the specified integration to execute.

Each action specifies the integration ID as well as a set of configuration used by the integration.

## Email

Email a set of recipients with the current status of the task.

**Integration ID**: `email`

**Configuration**

| Parameter | Description                                               |
|-----------|-----------------------------------------------------------|
| `to`      | Comma-separated list of recipient email addresses. Max 5. |

**Example Usage**

=== "Python"

    ```python
    action = Action(
        "success,error",
        integration=EmailIntegration(to="me@example.com")
    )
    task = Task.create(name="task name", actions=[action])
    ```

=== "Cli"

    ```shell
    taskbadger run "demo task" --action error,sucess email to:me@test.com -- path/to/script.sh
    ```

=== "Shell"

    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"name":"demo", "actions":[{"integration":"email","trigger":"success,error","config":{"to":"me@example.com"}}]}'
    ```

## Web Hook

The web hook integration allows you to call a URL with a task payload.

For security reasons web hooks must first be created on the web UI before they can be used
in task actions. This can be done by going to **Integrations** in the sidebar navigation.

Each web hook will have its own unique ID which is what will be used when creating actions.

**Integration ID**: `webhook:<slug>`

**Configuration**

There is currently no additional configuration required for Web Hooks other than
the configuration provided when creating them on the web.



**Example Usage**

=== "Python"

    ```python
    action = Action(
        "success,error",
        integration=WebhookIntegration(id="webhook:demo-123")
    )
    task = Task.create(name="task name", actions=[action])
    ```

=== "Cli"

    Since no additional configuration is required we must pass an empty string:

    ```shell
    taskbadger run "demo task" --action error,sucess webhook:demo-123 "" -- path/to/script.sh
    ```

=== "Shell"

    ```shell
    $ curl -X PATCH "https://taskbadger.net/api/${ORG}/${PROJECT}/tasks/" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{"name":"demo", actions":[{"integration":"webhook:demo-test","trigger":"success,error","config":{}}]}'
    ```
