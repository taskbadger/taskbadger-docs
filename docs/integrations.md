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

## Web Hook

The web hook integration allows you to call a URL with a task payload.

Web hooks must first be created in the web UI, under **Integrations** in the sidebar
navigation, before they can be used by an action.

**Integration ID**: `webhook:<slug>`

**Configuration**

There is currently no additional configuration required for web hooks other than
the configuration provided when creating them in the web UI. Each web hook has its own
unique ID (`webhook:<slug>`) which is used when referencing it from an action.
