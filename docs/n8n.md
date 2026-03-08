# n8n Setup Guide

Deploy CourierDB on Digital Ocean with your n8n for free and easy data storage and vectorization.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment](#deployment)
- [Connecting n8n to CourierDB](#connecting-n8n-to-courierdb)
- [Using CourierDB in n8n](#using-courierdb-in-n8n)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Digital Ocean Droplet with n8n already running via Docker
- SSH access to your droplet (using the console from the dashboard is simplest)
- CourierDB repository: [https://github.com/RecursionAI/CourierDB](https://github.com/RecursionAI/CourierDB)

## Deployment

### 1. SSH into your Digital Ocean droplet

Using console in the dashboard is easiest here. Just log in, go to your droplet, and click on the console

### 2. Clone CourierDB repository

```bash
cd /opt  # or wherever you want to store it
git clone https://github.com/RecursionAI/CourierDB.git
cd CourierDB
```

### 3. Configure your API key

Create your `.env` file:

```bash
touch .env
nano .env
```

#### Example `.env` file:

```ini
OPENAI_API_KEY = sk-proj-12345...
COURIERDB_API_KEY = my-super-secret-key
COURIERDB_PATH = ./my_db_storage
COURIERDB_VECTORIZER = openai
```

### 4. Start CourierDB

```bash
docker compose up -d
```

### 5. Verify CourierDB is running

```bash
docker ps
# Look for a CourierDB container
```

## Connecting n8n to CourierDB

### 1. Check container names

```bash
docker ps
```

You should see:

- `courierdb_server` (or similar)
- `n8n-docker-caddy-n8n` (or your n8n container name)

### 2. Check which networks they're on

```bash
docker inspect courierdb_server | grep -A 10 Networks
docker inspect n8n-docker-caddy-n8n | grep -A 10 Networks
```

### 3. Connect CourierDB to n8n's network

```bash
# Replace with your actual n8n network name (likely n8n-docker-caddy_default)
docker network connect n8n-docker-caddy_default courierdb_server
```

## Using CourierDB in n8n

Now that it's running you can start using CourierDB in n8n via the HTTP Request Node!

Here's a **comprehensive** guide on how you can use it.

### Schemas:

If you configured an API key you must always include an Authorization header in your requests with the value
`Bearer your-api-key`.

Look at the [Schemas](schemas.md) page for details on API schemas and url configurations.

### Creating/Updating Data (Upsert)

**Add an HTTP Request node in n8n:**/

- **Method:** `POST`
- **URL:** `http://courierdb_server:8000/v1/users/upsert`
- **Authentication:** Header Auth
    - Name: `Authorization`
    - Value: `Bearer your-api-key`
- **Body Content Type:** JSON
- **Body:**

```json
{
  "id": "unique-id-here",
  "data": {
    "name": "Example",
    "category": "AI Researcher",
    "content": "Your content here"
  }
}
```

**Important:** The `data` field must be a **single object**, not an array.

### Retrieving All Data

**HTTP Request node:**

- **Method:** `GET`
- **URL:** `http://courierdb_server:8000/v1/users`
- **Authentication:** Header Auth (same as above)
- **No body needed**

### Searching/Filtering Data

**HTTP Request node:**

- **Method:** `POST`
- **URL:** `http://courierdb_server:8000/v1/users/search`
- **Authentication:** Header Auth
- **Body:**

```json
{
  "query": {
    "category": "AI Researcher"
  }
}
```

### Example: Storing Multiple Items

If you have an array of items from a previous node, use a **Loop Over Items** or **Split Out** node first:

```
Your Data (array) 
  ↓
Split Out (on the array field)
  ↓
HTTP Request (Upsert)
  ↓
Each item saved individually
```

**In the HTTP Request body:**

```json
{
  "id": "{{ $json.id }}",
  "data": {{
  $json
}}
}
```

## Common Patterns

### Pattern 1: Store scraped data daily

```
Schedule Trigger (daily)
  ↓
Web Scraper
  ↓
Code: Add date and format
  ↓
HTTP Request: Upsert to CourierDB
```

### Pattern 2: Retrieve filtered content

```
Manual Trigger
  ↓
HTTP Request: Search CourierDB
  Body: { "query": { "category": "AI Researcher" } }
  ↓
Use results in next node
```

### Pattern 3: Newsletter workflow

```
Google Sheets (get subscribers)
  ↓
Loop Over Items (each subscriber)
  ↓
HTTP Request: Search CourierDB (filtered by their preferences)
  ↓
AI: Generate personalized email
  ↓
Gmail: Send email
```

## Troubleshooting

### Error: "ECONNREFUSED"

**Problem:** n8n can't reach CourierDB

**Solution:**

1. Verify both containers are running: `docker ps`
2. Check they're on the same network (see [Connecting n8n to CourierDB](#connecting-n8n-to-courierdb))
3. Use container name in URL: `http://courierdb:8000` or `http://courierdb_server:8000`

### Error: "Input should be a valid dictionary"

**Problem:** You're sending an array to the `data` field

**Solution:** CourierDB expects `data` to be a single object. If you have multiple items:

- Use Loop Over Items or Split Out to process one at a time
- Or wrap your array: `{ "id": "...", "data": { "items": [your array] } }`

### Error: "Input should be a valid string" (for id field)

**Problem:** The `id` field is receiving a number instead of a string

**Solution:** Convert to string: `"id": "{{ $json.id.toString() }}"` or use a string value directly

### CourierDB container keeps restarting

**Check logs:**

```bash
docker logs courierdb_server
```

Common issues:

- Missing API key in environment variables
- Port 8000 already in use
- Invalid docker-compose configuration

## File Locations

- **CourierDB installation:** `/opt/CourierDB` (or wherever you cloned it)
- **Data persistence:** Check your docker-compose.yml for volume mounts
- **Logs:** `docker logs courierdb_server`

## API Reference

For complete CourierDB API documentation, see: [CourierDB GitHub](https://github.com/RecursionAI/CourierDB)

## Related Documentation

- [n8n Official Docs](https://docs.n8n.io/)
- [Docker Networking](https://docs.docker.com/network/)
- [CourierDB Repository](https://github.com/RecursionAI/CourierDB)