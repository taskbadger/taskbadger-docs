---
hide:
  - navigation    
---

# Changelog

Full release notes for the Python SDK are available on [GitHub](https://github.com/taskbadger/taskbadger-python/releases).

## v2.3.0

**2026-07-23**

**Python SDK**

* **NEW** The Celery and Procrastinate integrations now automatically record the originating task/job ID on the task [`external_id`](data_model.md#external_id) field.

## v2.2.0

**2026-07-09**

**Python SDK**

* **DEPRECATED** Per-task actions are deprecated.
* **HOUSEKEEPING** Fix flaky Celery retry test.

## v2.1.0

**2026-07-08**

**Python SDK**

* **NEW** [Procrastinate integration](python-procrastinate.md) for automatically tracking Procrastinate jobs, including periodic tasks. Install with `pip install 'taskbadger[procrastinate]'`.
* **NEW** Tasks now have a [`queue`](data_model.md#queue) field, set automatically from the routing key (Celery) and task queue (Procrastinate). Also available on `create_task` / `update_task` and the CLI `create` / `update` commands.
* **HOUSEKEEPING** Dependency upgrades.

## v2.0.0

**2026-05-05**

**Python SDK**

* **BREAKING** CLI dependencies (`typer`, `rich`) are now an optional extra. Install with `pip install 'taskbadger[cli]'` (or `uv tool install 'taskbadger[cli]'`) to use the `taskbadger` command. SDK-only consumers no longer pull in these packages. The `typer` pin was also bumped from `<0.10` to `>=0.12`.
* **BREAKING** Removed the deprecated `task.update_progress` and `task.increment_progress` methods. Use `task.update_value` and `task.increment_value` instead (deprecated since v1.6.1).
* **BREAKING** Dropped support for Python 3.9. Minimum supported version is now Python 3.10.

## v1.7.0

**2026-02-16**

**Python SDK**

* **NEW** Support for [Project API Keys](basics.md#authentication) with automatic detection of organization and project from the key itself. The `organization_slug` / `project_slug` arguments to `taskbadger.init` are no longer required when using a project key.
* **UPDATE** Legacy API keys (which require explicit `organization_slug` and `project_slug`) now emit a `DeprecationWarning`. Migrate to Project API keys.
* **UPDATE** The CLI `configure` command now detects Project API keys and skips the organization/project prompts.

## v1.6.3

**2026-02-05**

**Python SDK**

* **NEW** Track Celery canvas primitives (`map`, `starmap`, `chunks`) so that inner tasks are recorded in Task Badger. More info in the [Celery docs](python-celery.md#canvas-primitives-map-starmap-chunks).

## v1.6.2

**2025-12-04**

**Python SDK**

* **HOUSEKEEPING** Remove upper bound on httpx dependency

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
