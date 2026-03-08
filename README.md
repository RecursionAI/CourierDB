# CourierDB

CourierDB is a JSON-first database with a simple HTTP API, Python SDK, and MCP interface.

## Core Features

- JSON document storage (NoSQL-style)
- Fast LMDB-backed persistence
- API key protection (optional)
- Docker-ready server
- MCP tools for agent workflows
- Python SDK for typed CRUD access

## Breaking Change

Vector and semantic features were removed.

- Removed USearch integration
- Removed embeddings/vectorization logic
- Removed `/v1/{collection}/search` API
- Removed SDK `search(...)`
- Removed MCP `courierdb_search`

## Getting Started

### GitHub

<https://github.com/RecursionAI/CourierDB>

### Docs

- [Install and Setup](./docs/install.md)
- [Python SDK](./docs/sdk.md)
- [n8n Guide](./docs/n8n.md)
- [API Schemas](./docs/schemas.md)
- [MCP Setup](./docs/mcp.md)
