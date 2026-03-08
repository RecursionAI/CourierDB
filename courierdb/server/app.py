import os
import base64
import uvicorn
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict

from courierdb.core.engine import CourierDB

load_dotenv()

db_instance: Optional[CourierDB] = None
DB_PATH = os.getenv("COURIERDB_PATH", "./flow_data")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_instance
    print(f"--- CourierDB Starting at {DB_PATH} ---")
    db_instance = CourierDB(storage_path=DB_PATH)
    async with mcp_asgi.lifespan(mcp_asgi):
        yield
    print("--- CourierDB Shutting Down ---")
    if db_instance:
        db_instance.close()


app = FastAPI(title="CourierDB", lifespan=lifespan)


class SecurityMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if path in ["/docs", "/openapi.json", "/favicon.ico"]:
            await self.app(scope, receive, send)
            return

        real_key = os.getenv("COURIERDB_API_KEY")
        if not real_key:
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        query_string = scope.get("query_string", b"").decode()

        input_key = None

        auth_header = headers.get(b"authorization", b"").decode()

        if auth_header.startswith("Bearer "):
            input_key = auth_header.split(" ")[1]
        elif auth_header.startswith("Basic "):
            try:
                encoded_creds = auth_header.split(" ")[1]
                decoded_bytes = base64.b64decode(encoded_creds)
                decoded_str = decoded_bytes.decode("utf-8")
                if ":" in decoded_str:
                    _, password = decoded_str.split(":", 1)
                    input_key = password
                else:
                    input_key = decoded_str
            except Exception:
                pass

        if not input_key:
            for param in query_string.split("&"):
                if param.startswith("api_key="):
                    input_key = param.split("=")[1]
                    break

        if input_key != real_key:
            await send({
                "type": "http.response.start",
                "status": 403,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({
                "type": "http.response.body",
                "body": b"Unauthorized: Invalid CourierDB API Key",
            })
            return

        await self.app(scope, receive, send)


app.add_middleware(SecurityMiddleware)


class GenericRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    data: Dict[str, Any]


def get_db():
    if not db_instance:
        raise HTTPException(500, "DB not initialized")
    return db_instance


@app.post("/v1/{collection_name}/upsert")
def rest_put(collection_name: str, payload: GenericRecord):
    col = get_db().collection(collection_name, GenericRecord)
    col.upsert(payload.id, payload)
    return {"status": "success", "id": payload.id}


@app.get("/v1/{collection_name}/read/{key}")
def rest_get(collection_name: str, key: str):
    col = get_db().collection(collection_name, GenericRecord)
    res = col.read(key)
    if not res: raise HTTPException(404, "Not found")
    return res


@app.get("/v1/{collection_name}/list")
def rest_list(collection_name: str, limit: int = 20, skip: int = 0):
    col = get_db().collection(collection_name, GenericRecord)
    return col.list(limit=limit, skip=skip)


@app.delete("/v1/{collection_name}/delete/{key}")
def rest_delete(collection_name: str, key: str):
    col = get_db().collection(collection_name, GenericRecord)
    deleted = col.delete(key)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "deleted", "id": key}


@app.get("/v1/collections")
def rest_list_collections():
    return {"collections": get_db().list_collections()}


# --- 2. The FastMCP Server ---
mcp = FastMCP("CourierDB Agent Interface")
mcp_asgi = mcp.http_app(path="/", transport="http")


@mcp.tool()
def courierdb_upsert(collection: str, key: str, data: Dict[str, Any]):
    """Create or Update a record in the database."""
    col = db_instance.collection(collection, GenericRecord)
    record = GenericRecord(id=key, data=data)
    col.upsert(key, record)
    return f"Successfully saved record {key} to collection {collection}"


@mcp.tool()
def courierdb_read(collection: str, key: str) -> str:
    """Read data from the database."""
    col = db_instance.collection(collection, GenericRecord)
    res = col.read(key)
    if not res: return "Error: Record not found."
    return str(res.data)


@mcp.tool()
def courierdb_list(collection: str, limit: int = 20, skip: int = 0) -> str:
    """List records in a collection."""
    col = db_instance.collection(collection, GenericRecord)
    results = col.list(limit=limit, skip=skip)
    if not results: return "No records found."
    summary = [f"ID: {r.id} | Data: {r.data}" for r in results]
    return "\n".join(summary)


@mcp.tool()
def courierdb_list_collections() -> str:
    """List all available collections."""
    names = db_instance.list_collections()
    if not names: return "No collections found."
    return "Available Collections:\n- " + "\n- ".join(names)


@mcp.tool()
def courierdb_delete(collection: str, key: str) -> str:
    """Delete a record by ID."""
    col = db_instance.collection(collection, GenericRecord)
    success = col.delete(key)
    if success:
        return f"Successfully deleted record {key} from {collection}."
    return f"Record {key} was not found."


app.mount("/mcp", mcp_asgi)


def start():
    uvicorn.run(
        "courierdb.server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ws="websockets-sansio",
    )


if __name__ == "__main__":
    start()
