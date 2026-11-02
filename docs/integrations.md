---
title: Integrations
---

# Integrations

Integrations are the channels that power [alerts](alerts.md) and [actions](actions.md). When an alert
fires it delivers a notification through the selected channel.

Channels are configured once in the web UI under **Alerts → Channels** and can be reused by
many alerts. Each channel has an ID (for example `email:ga-3`) which is used to reference it from an action.

## Email

Email a set of recipients with the current status of the task.

**Integration ID**: `email`

**Configuration**

| Parameter | Description                                               |
|-----------|-----------------------------------------------------------|
| `to`      | Comma-separated list of recipient email addresses. Max 5. |

## Slack

Post alerts to a Slack channel. Messages show the task name, status and progress, link back to the
task in Task Badger, and are colour-coded by status.

Slack must first be connected to your organization, and then a channel is created for each Slack
channel you want to post to. Alert messages for tasks, queue wait times and monitors are all supported.

**Integration ID**: `slack:<slug>`

**Connecting a workspace**

1. In the web UI, go to **Alerts** and under **Connections** select **Connect Slack**.
   Only organization admins can connect a workspace.
2. Approve the Task Badger app in Slack.

You can connect more than one workspace. Disconnecting a workspace removes any Slack channels that
used it and disables the alert rules that routed to them.

**Adding a Slack channel**

Under **Alerts → Channels**, select **Add channel**, choose Slack, and pick the Slack channel to post to.

| Parameter | Description                                                                                           |
|-----------|-------------------------------------------------------------------------------------------------------|
| Channel   | The Slack channel to post to. Public channels work without an invite; for private channels, invite the Task Badger bot first. |

Each Slack channel has its own unique ID (`slack:<slug>`) which is used when referencing it from an [action](actions.md).

**Routing alerts to different Slack channels**

To send alerts from different projects to different Slack channels, create one Slack channel per
destination and one [alert rule](alerts.md#task-rules) per project, setting the rule's **Project** filter and
choosing the matching Slack channel under **Notify via**. The **Name filter** can narrow this
further to tasks whose name matches a pattern.

**Message updates**

When a task that triggered an alert later changes state (for example, a `stale` task recovers or
completes), Task Badger edits the original Slack message to show the new state and adds a short
reply in its thread, rather than posting a separate message.

## Web Hook

The web hook integration allows you to call a URL with a task payload.

Web hooks must first be created in the web UI, under **Alerts → Channels**, before they can
be used by an alert or action.

**Integration ID**: `webhook:<slug>`

**Configuration**

There is currently no additional configuration required for web hooks other than
the configuration provided when creating them in the web UI. Each web hook has its own
unique ID (`webhook:<slug>`) which is used when referencing it from an action.
