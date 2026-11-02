---
title: Integrations
---

# Integrations

Integrations are the channels that power [actions](actions.md). When an action is triggered
it delivers a notification through the specified integration.

Integrations are configured once in the web UI under **Integrations** and can be reused by
many actions. Each integration has an ID which is used to reference it from an action.

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
channel you want to post to.

**Integration ID**: `slack:<slug>`

**Connecting a workspace**

1. In the web UI, go to **Integrations** and choose to add a Slack channel, then select
   **Connect Slack**. Only organization admins can connect a workspace.
2. Approve the Task Badger app in Slack.

You can connect more than one workspace. Disconnecting a workspace removes any Slack channels that
used it and disables the actions that routed to them.

**Adding a Slack channel**

Under **Integrations**, create a new Slack channel and pick the Slack channel to post to.

| Parameter | Description                                                                                           |
|-----------|-------------------------------------------------------------------------------------------------------|
| Channel   | The Slack channel to post to. Public channels work without an invite; for private channels, invite the Task Badger bot first. |

Each Slack channel has its own unique ID (`slack:<slug>`) which is used when referencing it from an action.

**Routing alerts to different Slack channels**

To send alerts from different projects to different Slack channels, create one Slack channel per
destination and one [action](actions.md) per project, setting the action's **Project** filter and
choosing the matching Slack channel under **Notify via**. The **Name filter** can narrow this
further to tasks whose name matches a pattern.

**Message updates**

When a task that triggered an alert later changes state (for example, a `stale` task recovers or
completes), Task Badger edits the original Slack message to show the new state and adds a short
reply in its thread, rather than posting a separate message.

## Web Hook

The web hook integration allows you to call a URL with a task payload.

Web hooks must first be created in the web UI, under **Integrations** in the sidebar
navigation, before they can be used by an action.

**Integration ID**: `webhook:<slug>`

**Configuration**

There is currently no additional configuration required for web hooks other than
the configuration provided when creating them in the web UI. Each web hook has its own
unique ID (`webhook:<slug>`) which is used when referencing it from an action.
