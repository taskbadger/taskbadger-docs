---
title: Actions
---
# Actions

Actions are at the core of Task Badger's alerting. They let you send notifications and
callouts based on task events — status changes, progress thresholds, or exceeding an
expected runtime.

Actions are configured in the Task Badger web UI and apply across your tasks, so you no
longer need to attach alerting to individual tasks in your code.

!!!note "Deprecation"
    Attaching actions to individual tasks via the SDK, CLI, or API is **deprecated** and
    will be removed in a future release. Configure actions in the web UI instead — see
    [Migrating from per-task actions](#migrating-from-per-task-actions).

## How actions work

An action combines two things:

- A **channel** — the reusable destination that delivers the notification (email, web hook).
  Channels are configured once under **Integrations** and can be reused by many actions.
- A **trigger** — the task event(s) that cause the action to fire.

When a task reaches a trigger point, Task Badger runs the action's channel with the current
task details.

## Channels

A channel is a reusable destination for notifications. See [Integrations](integrations.md)
for the available channel types and how to configure them.

## Creating an action

Actions are created in the web UI under **Integrations → Global Actions**.

Each action has the following settings:

| Setting        | Description                                                                          |
|----------------|--------------------------------------------------------------------------------------|
| Name           | A label to identify the action.                                                      |
| Project filter | Limit the action to a single project. Leave blank to apply to tasks in all projects. |
| Name filter    | A regular expression matched against the task name. Leave blank to match all tasks.  |
| Channel        | The [integration](integrations.md) used to deliver the notification.                 |
| Trigger        | The task event(s) that fire the action — see [Triggers](#triggers).                  |

Actions can be enabled or disabled at any time without deleting them.

## Triggers

A trigger is a comma-separated list of trigger points. Each trigger point is one of the following:

* A numeric value which is matched against the task `value`.
* A percentage value which is matched against the task `value_percent`.
* A task status which is matched against the task `status`.
* A special value `max_runtime_exceeded` which is matched when the task exceeds its `max_runtime` value.

Numeric and percentage trigger points can also be prefixed with `*/` to indicate that the trigger should
fire at regular intervals. For example, `*/50%` will fire at 0%, 50% and 100%.

Examples:

| Trigger               | Trigger Fire Points                                                          |
|-----------------------|------------------------------------------------------------------------------|
| `*/30%`               | When `value_percent` passes any multiple of 30%: 0%, 30%, 60%, 90%           |
| `success,error,stale` | When the state changes to any of the listed states                           |
| `95%,250,error`       | At 95%, when the value reaches or passes 250, when the state becomes `error` |

### Trigger edge cases

If a task value or status skips past multiple trigger points, only the last matching trigger will be
executed.

For example, an action configured with `20,40,80` whose value goes from `0` directly to `90` will
skip over the `20` and `40` events and only fire the `80` event. This also applies to task
status triggers.

This also applies to multiple trigger points that are reached simultaneously, for example, let's say
an action has the following trigger: `100,success`. It is quite likely that the task could reach
both those states at the same time but the action will only fire once.

## Migrating from per-task actions

Previously, actions were attached to individual tasks when they were created — via the
`actions` argument in the SDK, the `--action` option in the CLI, or the task `actions` field
in the API. This approach is **deprecated**: existing per-task actions keep working for now,
but the ability to create them will be removed in a future release.

To migrate, recreate your alerting as global actions in the web UI:

1. Configure the channels you need under **Integrations** (see [Integrations](integrations.md)).
2. Under **Integrations → Global Actions**, create an action for each alert you want, using a
   name filter and/or project filter to target the same tasks you previously attached actions to.

Global actions replace per-task actions entirely — a single action with a name filter can cover
every task that used to carry an inline action definition.
