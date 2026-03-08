## Client SDK

CourierDB includes a Python SDK for typed CRUD access.

### 1. Initialize

```python
from courierdb import CourierDB
from pydantic import BaseModel

# Connects to http://localhost:8000 by default
# Reads COURIERDB_API_KEY from env automatically if present
db = CourierDB()

# Or connect to remote
# db = CourierDB(url="http://164.x.x.x:8000", api_key="secret")
```

### 2. Define a model

```python
class Ticket(BaseModel):
    id: str
    title: str
    status: str
    description: str
```

### 3. Upsert (Create/Update)

```python
tickets = db.collection("tickets", Ticket)

new_ticket = Ticket(
    id="t-100",
    title="Login Broken",
    status="open",
    description="User cannot reset password on mobile."
)

tickets.upsert(new_ticket)
```

### 4. Read/List/Delete

```python
# Read by id
item = tickets.read("t-100")

# List with pagination
items = tickets.list(limit=20, skip=0)

# Delete by id
tickets.delete("t-100")
```

### 5. List collections

```python
print(db.list_collections())
# Example: ['tickets', 'users']
```

## Breaking Change

The SDK no longer provides semantic/vector search.
