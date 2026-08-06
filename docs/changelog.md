---
hide:
  - navigation    
---

# Changelog

Full release notes for the Python SDK are available on [GitHub](https://github.com/taskbadger/taskbadger-python/releases).

## v2.5.1

**2026-08-06**

**Python SDK**

* **CHANGED** [`list_tasks`](python.md#listing-tasks) returns a `TaskList` of `taskbadger.Task` objects, which can be iterated over directly. It previously returned the generated `PaginatedTaskList`, whose `results` were internal models without the SDK's update methods. Note that an empty `TaskList` is falsy, where `PaginatedTaskList` was always truthy.
* **FIX** Eager and canvas Celery tasks honour an explicit [`taskbadger_parent`](python-celery.md#subtasks), including `taskbadger_parent=None` to opt out of nesting.
* **FIX** Copying or pickling a `Task` no longer recurses until the stack overflows.

## v2.5.0

**2026-08-06**

**Python SDK**

* **NEW** [Parent and child tasks](python.md#parent-and-child-tasks). Tasks can be nested one level deep via the [`parent`](data_model.md#parent) field on `create_task` / `update_task`, and `list_tasks` can filter by parent. The [`@track` decorator](python-decorator.md#nested-tasks), [Celery](python-celery.md#subtasks) and [Procrastinate](python-procrastinate.md#subtasks) integrations set it automatically for tasks enqueued from within a tracked task.
* **NEW** [Context providers](python.md#error-context-providers), a pluggable way to attach extra data to a task when it errors, along with a [Sentry provider](python.md#sentry) that links a failed task to its Sentry issue. Install with `pip install 'taskbadger[sentry]'`.
* **NEW** `Task.error` accepts an `exception` argument, which is passed to the configured context providers.

## v2.4.0

**2026-07-30**

**Python SDK**

* **NEW** `heartbeat_interval` option for the [Celery](python-celery.md#keeping-long-running-tasks-fresh) and [Procrastinate](python-procrastinate.md#keeping-long-running-tasks-fresh) integrations. The worker updates running tasks for you so that long-running tasks don't go [`stale`](data_model.md#stale_timeout).
* **FIX** An eager Celery task no longer closes a Task Badger session opened by its caller.

## v2.3.1

**2026-07-27**

**Python SDK**

* **FIX** Guard against unregistered task in `before_task_publish` handler.

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
