## Using the MCP server

CourierDB provides an MCP endpoint at `/mcp` (Streamable HTTP transport).

## What tools are available

- `courierdb_upsert(collection, key, data)`
- `courierdb_read(collection, key)`
- `courierdb_list(collection, limit=20, skip=0)`
- `courierdb_list_collections()`
- `courierdb_delete(collection, key)`

## Claude Desktop Setup

### 1. Install bridge tool

```bash
pip install fastmcp
```

### 2. Configure Claude Desktop

Edit config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Example:

```json
{
  "preferences": {
    "menuBarEnabled": false,
    "quickEntryShortcut": "off"
  },
  "mcpServers": {
    "courierdb": {
      "command": "/Users/<user>/.pyenv/shims/fastmcp",
      "args": [
        "run",
        "http://:<API_KEY>@localhost:8000/mcp"
      ]
    }
  }
}
```

If API key auth is disabled, use `http://localhost:8000/mcp`.

## Breaking Change

The MCP tool `courierdb_search` was removed with vector/semantic support.
