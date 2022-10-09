---
title: API Endpoints
---
* Create task
  * with / without actions 
* Update task
* List tasks
* Cancel task
* Add task action
* Cancel task action



# Actions

Actions are at the core of Task Badger's secret sauce. They allow you to send notifications, callouts,
and more based on task events.

Every action specifies an integration e.g. `email`, and a trigger definition which is
like a crontab expression, but for tasks. For example, `*/25%,success` means, "execute
this action when the task value passes 25%, 50%, 75%, 100% and when the task status
is set to `success`".

A task may have multiple actions, each with their own integration and trigger definition.

## Edge cases

If a task value or status skips past multiple trigger points all but the last trigger will be skipped.

For example, an action configured with `20,40,80` whose value goes from `0` directly to `90` will
skip over the `20` and `40` events and only fire the `80` event. This also applies to task
status triggers.
