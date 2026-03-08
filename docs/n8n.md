# n8n Setup Guide

Deploy CourierDB next to n8n for simple JSON persistence.

## Prerequisites

- n8n running via Docker
- SSH access to your server
- CourierDB repository: <https://github.com/RecursionAI/CourierDB>

## Deploy CourierDB

### 1. Clone

```bash
cd /opt
git clone https://github.com/RecursionAI/CourierDB.git
cd CourierDB
```

### 2. Configure `.env`

```ini
# COURIERDB Configuration
COURIERDB_PATH=./flow_data

# Keys
COURIERDB_API_KEY=fdb-45hg8b4-ivob4v3vb4
```

`COURIERDB_API_KEY` is optional.

### 3. Start

```bash
docker compose up -d
```

### 4. Verify

```bash
docker ps
```

## Connect to n8n network

```bash
docker inspect courierdb_server | grep -A 10 Networks
docker inspect <your_n8n_container> | grep -A 10 Networks
docker network connect <n8n_network> courierdb_server
```

## Use CourierDB in n8n

If API key auth is enabled, send header:

```http
Authorization: Bearer <your-api-key>
```

### Upsert

- Method: `POST`
- URL: `http://courierdb_server:8000/v1/users/upsert`
- Body:

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

### Read

- Method: `GET`
- URL: `http://courierdb_server:8000/v1/users/read/unique-id-here`

### List

- Method: `GET`
- URL: `http://courierdb_server:8000/v1/users/list?limit=20&skip=0`

### Delete

- Method: `DELETE`
- URL: `http://courierdb_server:8000/v1/users/delete/unique-id-here`

### List collections

- Method: `GET`
- URL: `http://courierdb_server:8000/v1/collections`

## Breaking Change

Vector and semantic-search endpoints were removed. n8n workflows should use CRUD/list endpoints only.
