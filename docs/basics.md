---
title: Using the API
---
# Using the Task Badger API

## Organization and Project

API endpoints include both the `organization` and `project` slug. The user authenticating
the request must have access to both for the request to be accepted.

## Authentication

Requests must be authenticated by providing a bearer token provided
in the Authentication header.

```linenums="1" hl_lines="2"
POST https://taskbadger.net/api/{organization}/{project}/tasks/
Authorization: Bearer xxxx
Content-type: application/json
{"name":"demo task","status":"pending"}
```

## Request bodies

The payload of HTTP POST requests must be specified as JSON. 
The Content-type HTTP header must be set to `application/json`
Without this header the data won't be interpreted as JSON.

For example:

```linenums="1" hl_lines="3 4"
POST https://taskbadger.net/api/{organization}/{project}/tasks/
Authorization: Bearer xxxx
Content-type: application/json
{"name":"demo task","status":"pending"}
```

## Request methods

Task Badger uses standard REST methods: 

| Method | Function                                      |
|--------|-----------------------------------------------|
| GET    | Retrieve an object or list of objects         |
| POST   | Create an object                              |
| PUT    | Update an object (complete data required)     |
| PATCH  | Update an object (partial data required)      |
| DELETE | Delete or mark object as deleted or cancelled |

## Pagination

List requests use cursor pagination. Each request will include a `next` and `previous` field. These may be null
indicating that is no next or previous page but will otherwise contain the full URL of the page.

The cursors can be used to navigate forwards or backwards through the data. For example:

```
GET https://taskbadger.net/api/{organization}/{project}/tasks/?page_size=2
```

This will respond with tasks in pages of size 2:

```json
{
  "previous": null,
  "next": "https://taskbadger.net/api/{organization}/{project}/tasks/?cursor=XXX&page_size=2",
  "results": [{...}, {...}]
}
```

To access the next page of data make a request to the URL provided in the `next` field:

```
GET https://taskbadger.net/api/{organization}/{project}/tasks/?cursor=XXX&page_size=2
```

The response will now include both `next` and `previous` page URLs.

```json
{
  "previous": "https://taskbadger.net/api/{organization}/{project}/tasks/?cursor=YYY&page_size=2",
  "next": "https://taskbadger.net/api/{organization}/{project}/tasks/?cursor=ZZZ&page_size=2",
  "results": [{...}, {...}]
}
```

!!!tip

    The `page_size` parameter can be changed at any point to adjust the page size of the request.


## Rate Limiting

Rate limits are applied to API requests based on the Organization subscription plan. Requests
that have been rate limited will respond as follows:

```linenums="1"
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

[//]: # (## API Responses)
[//]: # (TODO See https://api.slack.com/web#slack-web-api__evaluating-responses)

## OpenAPI Specification

The Task Badger API includes an endpoint for downloading the OpenAPI 2.0 specification which describes
the requests and responses.

Download the spec from [taskbadger.net](https://taskbadger.net/api/schema.json){:target="_blank"}
