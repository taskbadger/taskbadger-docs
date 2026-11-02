---
title: Actions
---
# Actions

Actions are the older, **per-task** way of sending notifications. An action is attached to an
individual task when it is created or updated — via the `actions` argument in the SDK, the
`--action` option in the CLI, or the task `actions` field in the API — and runs a
[channel](integrations.md) when the task reaches one of its trigger points.

!!!note "Deprecation"
    Attaching actions to individual tasks via the SDK, CLI, or API is **deprecated** and
    will be removed in a future release. Configure [alerts](alerts.md) in the web UI instead — see
    [Migrating from actions](alerts.md#migrating-from-actions).

Existing actions keep working. An action has two parts:

- A **channel** — the destination that delivers the notification, such as email, Slack or a web hook.
  See [Integrations](integrations.md).
- A **trigger** — the task event(s) that cause the action to fire. Triggers use the same syntax
  as alert triggers, see [Triggers](alerts.md#triggers).

The API endpoints for listing, adding, updating and cancelling the actions on a task are listed
in the [API](api.md) docs.

## Alerts

[Alerts](alerts.md) are configured in the web UI rather than per task. They support the same
triggers and channels, can apply to all tasks in a project or those matching a name, and also cover
queue wait times and monitors. Use alerts for new work.
