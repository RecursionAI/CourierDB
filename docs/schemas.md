# API Schemas

CourierDB is API-controlled. Base URL defaults to `http://localhost:8000`.

## Auth

If `COURIERDB_API_KEY` is configured, include:

```http
Authorization: Bearer <API_KEY>
```

## Endpoints

### Upsert

**POST** `/v1/{collection_name}/upsert`

Body:

```json
{
  "id": "user-1",
  "data": {
    "name": "Ada",
    "role": "admin"
  }
}
```

### Read

**GET** `/v1/{collection_name}/read/{key}`

### List

**GET** `/v1/{collection_name}/list?limit=20&skip=0`

### Delete

**DELETE** `/v1/{collection_name}/delete/{key}`

### List Collections

**GET** `/v1/collections`

Response:

```json
{
  "collections": ["users", "tickets"]
}
```

## Breaking Change

`POST /v1/{collection_name}/search` was removed.
