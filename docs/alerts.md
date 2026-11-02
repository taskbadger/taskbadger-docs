---
title: Alerts
---
# Alerts

Alerts notify you when tasks fail, queues back up, or a scheduled job doesn't check in. They
are configured in the Task Badger web UI under **Alerts** in the sidebar, apply across your
tasks, and are routed to the channels your team already uses (email, Slack, web hooks).

Because alerts live in the web UI you don't need to change any code to add or change them.

!!!note "Alerts vs. actions"
    [Actions](actions.md) are the older, per-task mechanism: they are attached to individual
    tasks via the API, SDK or CLI. Alerts replace them. See
    [Migrating from actions](#migrating-from-actions).

The **Alerts** page has three sections:

| Section         | Purpose                                                                           |
|-----------------|-----------------------------------------------------------------------------------|
| **Alert Rules** | When something happens, notify a channel. Task, queue and monitor alerts live here. |
| **Channels**    | Where alerts get sent. A channel can be reused across many rules.                 |
| **Connections** | Connected apps, e.g. a Slack workspace.                                           |

## Alert rules

Create a rule with **New rule**. Each rule is shown with its type, what it triggers on, and
the channel it notifies. Rules can be edited, paused and resumed, or deleted. A paused rule
is kept but never fires.

There are two kinds of rule, labelled in the list:

* **Task** rules fire on events for individual tasks, such as a task failing or going stale.
* **Metric** rules fire when a measured value crosses a threshold, such as the average queue wait.

Alerts for [monitors](monitors.md) (a scheduled job that doesn't check in) are managed on the
same page.

### Task rules

A task rule has the following settings:

| Setting        | Description                                                                          |
|----------------|--------------------------------------------------------------------------------------|
| Name           | A label to identify the rule.                                                        |
| Project        | Only trigger for tasks in this project. Leave blank to apply to all projects.        |
| Name filter    | A regular expression matched against the task name. Leave blank to match all tasks.  |
| Notify via     | The [channel](#channels) used to deliver the notification.                           |
| Action Trigger | The task event(s) that fire the rule — see [Triggers](#triggers).                    |

For example, a rule with the trigger `error,max_runtime_exceeded,queue_wait_exceeded` notifies
you when any task fails, runs for longer than its `max_runtime`, or waits in the queue
longer than its threshold, and a second rule with the trigger `stale` can notify a different
channel when tasks go stale.

### Metric rules

A metric rule watches a value across a queue rather than a single task. For example, an
**Avg queue wait** rule fires when the average time tasks spend waiting to start rises above a
threshold (`avg wait > 5s`). The alert re-notifies the channel when the metric recovers.

## Triggers

A trigger is a comma-separated list of trigger points. Each trigger point is one of the following:

* A numeric value which is matched against the task `value`.
* A percentage value which is matched against the task `value_percent`.
* A task status which is matched against the task `status`.
* A special value `max_runtime_exceeded` which is matched when the task exceeds its `max_runtime` value.
* A special value `queue_wait_exceeded` which is matched when the task has waited in the queue longer than its threshold.

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

For example, a rule configured with `20,40,80` whose value goes from `0` directly to `90` will
skip over the `20` and `40` events and only fire the `80` event. This also applies to task
status triggers.

This also applies to multiple trigger points that are reached simultaneously, for example, let's say
a rule has the following trigger: `100,success`. It is quite likely that the task could reach
both those states at the same time but the rule will only fire once.

## Channels

A channel is a reusable destination for alerts. Add one with **Add channel**. Each channel has an
ID (for example `email:ga-3` or `slack:ocs-ops-slack`) shown on the page. See
[Integrations](integrations.md) for the available channel types and how to configure them.

## Connections

Connections link Task Badger to an external app. Use **Connect Slack** to connect a Slack
workspace once, then create any number of Slack channels that post to channels in it. See
[Slack](integrations.md#slack).

## Migrating from actions

Previously, [actions](actions.md) were attached to individual tasks when they were created. This
approach is **deprecated**: existing actions keep working for now, but the ability to create
them will be removed in a future release.

To migrate:

1. Configure the channels you need under **Alerts → Channels**.
2. Under **Alerts → Alert Rules**, create a task rule for each alert you want, using a
   name filter and/or project to target the same tasks you previously attached actions to.

A single rule with a name filter can cover every task that used to carry an inline action definition.
