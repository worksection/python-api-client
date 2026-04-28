# Worksection Python API Client

Official Python client library for the [Worksection](https://worksection.com) API.

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)

## Installation

```bash
pip install worksection-api-client
```

## Authentication

The client supports two authentication methods: **API Key** (admin access) and **OAuth2** (user access).

### API Key

Get your API key from your Worksection account settings.

```python
from worksection import Client

client = Client('https://your-account.worksection.com')
client.set_api_key('your-api-key')
```

### OAuth2

```python
from worksection import Client

client = Client('https://your-account.worksection.com')
client.set_client({
    'client_id':     'your-client-id',
    'client_secret': 'your-client-secret',
    'redirect_uri':  'https://your-app.com/callback',
    'scope':         ['projects_read', 'tasks_read', 'tasks_write'],
    # defaults:
    'auth_url':      'https://worksection.com/oauth2/authorize',
    'token_url':     'https://worksection.com/oauth2/token',
    'refresh_url':   'https://worksection.com/oauth2/refresh',
})

# Step 1: redirect the user to the authorization URL
import secrets
state = secrets.token_hex(16)
auth_url = client.oauth.get_authorization_url(state)
# redirect user to auth_url

# Step 2: exchange the authorization code for an access token (in your callback handler)
if request.args['state'] != state:
    raise Exception('Invalid state')
token = client.oauth.fetch_access_token_by_auth_code(request.args['code'])
client.set_access_token(token)

# The client will automatically refresh the access token using the refresh token when needed.
```

#### Available OAuth2 scopes

`projects_read`, `projects_write`, `tasks_read`, `tasks_write`, `costs_read`, `costs_write`,
`tags_read`, `tags_write`, `comments_read`, `comments_write`, `files_read`, `files_write`,
`users_read`, `users_write`, `contacts_read`, `contacts_write`, `administrative`

## Usage

### Projects

```python
# List all projects
projects = client.projects.list()

# Filter projects: active | pending | archived
active = client.projects.list({'filter': 'active'})

# Get a single project
project = client.projects.get(project_id)

# Create a project
project = client.projects.create('Project title', {
    'email_manager': 'manager@example.com',
    'dateend':       '2025-12-31',
})

# Update a project
project = client.projects.update(project_id, {'title': 'New title'})

# Archive / activate
client.projects.close(project_id)
client.projects.activate(project_id)

# Manage members
client.projects.add_members(project_id, ['user@example.com'])
client.projects.remove_members(project_id, ['user@example.com'])

# Project groups (folders)
groups = client.projects.groups()
group  = client.projects.create_group('Group name')

# Tags
tags = client.projects.tags()
tag  = client.projects.create_tag(group_id, 'Tag name')
client.projects.update_tags(project_id, add_ids=[1, 2], remove_ids=[3])

# Tag groups
tag_groups = client.projects.tag_groups()
tag_group  = client.projects.create_tag_group('Group name', access='public')

# Custom fields
fields = client.projects.custom_fields()
```

### Tasks

```python
# List tasks in a project
tasks = client.tasks.list(project_id)

# List all tasks across all projects
tasks = client.tasks.list()

# Get a single task (with extra data)
task = client.tasks.get(task_id, {'extra': 'text,files,comments'})

# Create a task
task = client.tasks.create(project_id, 'Task title', {
    'email_user_to': 'assignee@example.com',
    'dateend':       '2025-06-30',
    'priority':      'high',
    'files':         uploaded_files,  # check Files section for upload method
})

# Create a subtask
subtask = client.tasks.create(project_id, 'Subtask title', {
    'id_parent': parent_task_id,
})

# Update a task
task = client.tasks.update(task_id, {'title': 'New title'})

# Complete / reopen
client.tasks.complete(task_id)
client.tasks.reopen(task_id)

# Search tasks
tasks = client.tasks.search({'email_user_to': 'user@example.com', 'status': 'active'})

# Subscribers
client.tasks.subscribe(task_id, 'user@example.com')
client.tasks.unsubscribe(task_id, 'user@example.com')

# Tags
tags = client.tasks.tags()
tag  = client.tasks.create_tag(group_id, 'Tag name')
client.tasks.update_tags(task_id, add_ids=[1, 2], remove_ids=[3])

# Tag groups
tag_groups = client.tasks.tag_groups()
tag_group  = client.tasks.create_tag_group('Group name', type='status', access='public')

# Custom fields
fields = client.tasks.custom_fields()
```

### Comments

```python
# List comments on a task
comments = client.comments.list(task_id)

# List comments with attached files
comments = client.comments.list(task_id, {'extra': 'files'})

# Create a comment
comment = client.comments.create(task_id, 'Comment text', {
    'email_user_from': 'author@example.com',
    'hidden':          1,  # internal comment
})
```

### Members

```python
# List all account members
members = client.members.list()

# Invite a new member
member = client.members.create('newuser@example.com', {
    'first_name': 'John',
    'last_name':  'Doe',
    'title':      'Developer',
    'role':       'user',  # user | manager | admin
})

# Member groups (teams)
groups = client.members.groups()
group  = client.members.create_group('Backend Team')

# Work schedules
schedules = client.members.schedule({
    'users':     ['user@example.com'],
    'datestart': '2025-01-01',
    'dateend':   '2025-01-31',
})

client.members.update_schedule({
    'user@example.com': {'mon': 8, 'tue': 8, 'wed': 8, 'thu': 8, 'fri': 8},
})
```

### User (OAuth2 only)

```python
# Get the current authenticated user's profile
profile = client.user.profile()

# Timer management for the current user
timer = client.user.timer()                   # get active timer (or None)
client.user.start_timer(task_id)              # start timer on a task
client.user.stop_timer('Done for today')      # stop and log with a comment
client.user.discard_timer()                   # discard without logging
```

### Costs

```python
# List expense records
costs = client.costs.list()

# Filter by project, task, or date range
costs = client.costs.list({
    'id_project': project_id,
    'datestart':  '2025-01-01',
    'dateend':    '2025-01-31',
})

# Get totals/summary
total = client.costs.total({'id_project': project_id})

# Get totals broken down by project and task
total = client.costs.total({'extra': 'projects,tasks'})

# Create an expense record
cost_id = client.costs.create(task_id, {
    'time':            90,
    'money':           50,
    'email_user_from': 'user@example.com',
    'comment':         'Design work',
    'date':            '15.06.2025',
})

# Update / delete
client.costs.update(cost_id, {'time': 120, 'comment': 'Updated'})
client.costs.delete(cost_id)
```

### Timers (admin)

```python
# List all active timers across the account
timers = client.timers.all()

# Stop a specific timer
client.timers.stop(timer_id)
```

### Contacts

```python
# List all contacts
contacts = client.contacts.list()

# Create a contact
contact = client.contacts.create('client@example.com', 'Jane Smith', {
    'title':   'CEO',
    'group':   group_id,
    'phone':   '+1 555 000 0000',
    'address': '123 Main St',
})

# Contact groups
groups = client.contacts.groups()
group  = client.contacts.create_group('VIP Clients')
```

### Events

```python
# Get recent events for the whole account
events = client.events.list('7d')

# Get events for a specific project
events = client.events.list('30d', project_id)
```

### Files

```python
# List files on a task
files = client.files.list({'id_task': task_id})

# List files in a project
files = client.files.list({'id_project': project_id})

# Upload files (array of absolute local paths)
uploaded = client.files.upload([
    '/home/user/files/photo.jpg',
    '/home/user/files/document.txt',
])

# specify ID of the file and a destination local path
downloaded = client.files.download(file_id, '/home/user/downloads/tmp_file_1')
```

### Webhooks

```python
# List all webhooks
webhooks = client.webhook.list()

# Create a webhook
# Available events: post_task, post_comment, post_project,
#                   update_task, update_comment, update_project,
#                   delete_task, delete_comment, close_task
id = client.webhook.create(
    'https://your-app.com/webhook',
    ['post_task', 'update_task', 'close_task'],
    {'projects': [project_id]},
)

# Delete a webhook
client.webhook.delete(id)
```

## Error handling

```python
from worksection import ResponseException, UnauthorizedException

try:
    task = client.tasks.get(task_id)
except UnauthorizedException as e:
    # Invalid or expired token
    pass
except ResponseException as e:
    # API returned an error response
    print(e, e.status_code)
```

## License

MIT