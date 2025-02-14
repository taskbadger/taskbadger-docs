---
hide:
  - navigation    
---

# Changelog

## v1.5.0

**2025-02-14**

* **NEW** Tasks now support tagging. Tags are useful for categorizing tasks and filtering them in the UI. See [Task Tags](data_model.md#tags) for more information.

**Python SDK**

* **NEW** Support for tagging.
* **NEW** `before_create` callback to allow modification of task data before it is created. This is useful for adding global tags and metadata to tasks such as the current tenant etc. See [Before Create Callback](python.md#before-create-callback) for more information.
