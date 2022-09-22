---
sidebar_position: 1
title: Quick Start
slug: /
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get the Badger working!

Let's discover **Task Badger in less than 5 minutes**.

## Creating a task

Creating a task is very simple. Make a POST request to the API with the task
data.

<Tabs groupId="api-examples">
<TabItem value="shell" label="Shell">

```shell
$ curl -X POST https://taskbadger.net/api/0/{organization}/{project}/tasks/ \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "demo task", "status": "pending"}'
```

</TabItem>
</Tabs>

The response will include the task ID which is needed for updating the task.

```json title=Response
{
  "id": "{task-id}",
  "organization":"{organization}",
  "project": "{project}",
  "name":"demo task",
  "status":"pending",
  "value":null,
  "data":null,
  "created":"2022-09-22T06:53:40.683555Z",
  "updated":"2022-09-22T06:53:40.683555Z"
}
```

The task will now be listed in the task list: https://taskbadger.net/a/{organization}/tasks/.

## Update task progress

Here we update the task `status` and `value`. By default, a task's value can range from
0 to 100.

<Tabs groupId="api-examples">
<TabItem value="shell" label="Shell">

```shell title=Request
$ curl -X PATCH https://taskbadger.net/api/0/{organization}/{project}/tasks/{task-id} \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "pending", "value": 5}'
```

</TabItem>
</Tabs>

## Mark the task complete

When the task is complete update the status to either `success` or `error`.
The value may also be updated to 100.

<Tabs groupId="api-examples">
<TabItem value="shell" label="Shell">

```shell title=Request
$ curl -X PATCH https://taskbadger.net/api/0/{organization}/{project}/tasks/{task-id} \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "success", "value": 100}'
```

</TabItem>
</Tabs>
