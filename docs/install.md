
### Installation

#### Client SDK:

```bash
pip install courierdb
```

#### Server:
git clone the repo to spin up your local dev server or production dockerized server.

-----

### Configuration

CourierDB is configured via a `.env` file in your project root or via Environment Variables.

This is where you set your OpenAI API key for auto-vectorization and your CourierDB API key for database protection.

| Variable            | Description                                            | Required? | Default              |
|:--------------------|:-------------------------------------------------------|:----------|:---------------------|
| `OPENAI_API_KEY`    | Your OpenAI Key for auto-vectorization.                | **Yes**   | `None`               |
| `COURIERDB_API_KEY`    | Secures the DB. If set, clients must provide this key. | No        | `None` (Open Access) |
| `COURIERDB_PATH`       | Where data files are stored on disk.                   | No        | `./flow_data`        |
| `COURIERDB_VECTORIZER` | Provider to use (`openai` or `mock`).                  | No        | `auto`               |

**Example `.env` file:**

```ini
OPENAI_API_KEY = sk-proj-12345...
COURIERDB_API_KEY = my-super-secret-password
COURIERDB_PATH = ./my_db_storage
COURIERDB_VECTORIZER = openai
```

-----

For running the server locally simply run:

```bash
courierdb start
```

CourierDB defaults to Uvicorn's `websockets-sansio` backend to avoid legacy `websockets` deprecation warnings.
If needed, override via `courierdb start --ws auto|none|websockets|websockets-sansio|wsproto`.

For production navigate to the root CourierDB directory and run:

```bash
docker-compose up -d
```

This creates an API on port 8000 ready for reads and writes. The client SDK will automaticlaly read and write to this
port. If using API key configure a COURIERDB_API_KEY in your `.env` file and the client SDK should just work.
