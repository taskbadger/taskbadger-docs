---
hide:
  - navigation    
---

# Changelog

## v1.6.1

**2025-03-04**

**Python SDK**

* **UPDATE** Deprecate `task.update_progress` and `task.increment_progress` in favour of `task.update_value` and `task.increment_value`.
* **UPDATE** Return boolean from `task.udpate_value` and `task.ping` to indicate whether an update was made.

## v1.6.0

**2025-03-03**

**Python SDK**

* **NEW** Add optional rate limiting for task updates when calling `task.ping` and `task.update_progress`

## v1.5.0

**2025-02-14**

* **NEW** Tasks now support tagging. Tags are useful for categorizing tasks and filtering them in the UI. See [Task Tags](data_model.md#tags) for more information.

**Python SDK**

* **NEW** Support for tagging.
* **NEW** `before_create` callback to allow modification of task data before it is created. This is useful for adding global tags and metadata to tasks such as the current tenant etc. See [Before Create Callback](python.md#before-create-callback) for more information.

## v1.4.0

**2025-02-10**

**Python SDK**

* **NEW** Add option to `CelerySystemIntegration` to automatically record Celery task arguments in task data.
