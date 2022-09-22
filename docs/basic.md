---
title: Using the API
slug: /api-basics
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Using the Task Badger API


## Organization and Project

API endpoints include both the `organization` and `project` slug. The user authenticating
the request must have access to both for the request to be accepted.

## Authentication

Requests must be authenticated by providing a bearer token provided
in the Authentication header.

```- showLineNumbers
POST https://taskbadger.net/api/0/{organization}/{project}/tasks/
// highlight-next-line
Authorization: Bearer xxxx
Content-type: application/json
{"name":"demo task","status":"pending"}
```

## POST Bodies

The payload of HTTP POST requests may be specified as either standard POST parameters
or JSON.

### URL-encoded bodies
When sending URL-encoded data, the HTTP `Content-Type` header should be set
to `application/x-www-form-urlencoded`. 

For example:

```- showLineNumbers
POST https://taskbadger.net/api/0/{organization}/{project}/tasks/
Authorization: Bearer xxxx
// highlight-start
Content-type: application/x-www-form-urlencoded
name=demo%20task&status=pending
// highlight-end
```

### JSON-encoded bodies

POST data may also be sent in JSON-encoded format. The Content-type HTTP header must be set to `application/json`
Without this header the data won't be interpreted as JSON.

For example:

```- showLineNumbers
POST https://taskbadger.net/api/0/{organization}/{project}/tasks/
Authorization: Bearer xxxx
// highlight-start
Content-type: application/json
{"name":"demo task","status":"pending"}
// highlight-end
```

## Pagination

List requests use cursor pagination. Each request will include a `next` and `previous` field. These may be null
indicating that is no next or previous page but will otherwise contain the full URL of the page.

The cursors can be used to navigate forwards or backwards through the data. For example:

```
GET https://taskbadger.net/api/0/{organization}/{project}/tasks/?limit=2
```

This will respond with tasks in pages of size 2:

```json
{
  "previous": null,
  "next": "https://taskbadger.net/api/0/{organization}/{project}/tasks/?cursor=XXX&limit=2",
  "results": [{...}, {...}]
}
```

To access the next page of data make a request to the URL provided in the `next` field:

```
GET https://taskbadger.net/api/0/{organization}/{project}/tasks/?cursor=XXX&limit=2
```

The response will now include both `next` and `previous` page URLs.

```json
{
  "previous": "https://taskbadger.net/api/0/{organization}/{project}/tasks/?cursor=YYY&limit=2",
  "next": "https://taskbadger.net/api/0/{organization}/{project}/tasks/?cursor=ZZZ&limit=2",
  "results": [{...}, {...}]
}
```

:::tip

The `limit` parameter can be changed at any point to adjust the page size of the request.

:::

[//]: # (TODO)

## Rate Limiting

Rate limits are applied to API requests based on the Organization subscription plan. Requests
that have been rate limited will respond as follows:

```- showLineNumbers
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

[//]: # (## API Responses)
[//]: # (TODO See https://api.slack.com/web#slack-web-api__evaluating-responses)

## OpenAPI Specification

The Task Badger API includes an endpoint for downloading the OpenAPI 2.0 specification which describes
the requests and responses.

Download the spec from [taskbadger.net](https://taskbadger.net/api/schema.json)
