---
title: Integrations
---

# Integrations

Task Badger integrations are what power the actions. When an action is triggered it causes
the specified integration to execute.

Each action specifies the integration ID as well as a set of configuration used by the integration.

## Email

Send an email to a set of recipients with the current status of the task.

**Integration ID**: `email`

**Configuration**

| Parameter | Description                                               |
|----------|-----------------------------------------------------------|
| `to`       | Comma-separated list of recipient email addresses. Max 5. |
