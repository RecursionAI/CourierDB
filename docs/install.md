## Installation

### Client SDK

```bash
pip install courierdb
```

### Server

Clone the repo and run locally or with Docker.

## Configuration

CourierDB reads configuration from `.env` (or environment variables).

Supported variables:

| Variable | Description | Required? | Default |
|:--|:--|:--|:--|
| `COURIERDB_PATH` | Where data files are stored on disk. | No | `./flow_data` |
| `COURIERDB_API_KEY` | If set, all API requests must provide this key. | No | `None` (open access) |

Example `.env`:

```ini
# COURIERDB Configuration
COURIERDB_PATH=./flow_data

# Keys
COURIERDB_API_KEY=fdb-45hg8b4-ivob4v3vb4
```

## Run Locally

```bash
courierdb start
```

CourierDB defaults to Uvicorn's `websockets-sansio` backend.
You can override with `courierdb start --ws auto|none|websockets|websockets-sansio|wsproto`.

## Run with Docker

From repo root:

```bash
docker compose up -d
```

This starts the API on port `8000` and persists data in `./flow_data`.
