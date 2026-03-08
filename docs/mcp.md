## Using the MCP server

CourierDB is **MCP-Native**. This allows **Claude Desktop** to natively "see", "search", and "edit" your database without any custom glue code.

**What this enables:**
You can ask Claude: *"Check the 'tickets' collection for any high-priority bugs regarding login issues, and summarize them for me."*

### Step 1: Install the Bridge Tool

We use `fastmcp` to bridge Claude (Stdio) to CourierDB (HTTP).

```bash
pip install fastmcp
```

### Step 2: Configure Claude

Edit your config file:

  * **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
  * **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Update it like this:

```json
{
  "preferences": {
    "menuBarEnabled": false,
    "quickEntryShortcut": "off"
  },
  "mcpServers": {
    "courierdb": {
      "command": "/Users/<user>/.pyenv/shims/fastmcp", // path-to-fastmcp
      "args": [
        "run",
        "http://:<API_KEY>@localhost:8000/mcp"
      ]
    }
  }
}


```

> **Note on Security:** We pass the API Key in the URL format `http://:PASSWORD@HOST` (Basic Auth style). Replace `YOUR_API_KEY` with the key from your `.env` file. If you haven't set a key (Dev Mode), use `http://localhost:8000/mcp`.

> **Breaking change (v0.2.0):** CourierDB now uses Streamable HTTP MCP at `/mcp`. Legacy SSE endpoints `/mcp/sse` and `/mcp/messages` are removed.
