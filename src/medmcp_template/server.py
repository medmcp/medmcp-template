"""MCP server entrypoint for medmcp-template.

Replace this module's tool registrations with your domain tools after
scaffolding a new repo from the template. See README.md for the full workflow.
"""

import multiprocessing
import os
import sys
from importlib.resources import files as _pkg_files
from typing import TextIO

import anyio
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

from medmcp_template.effects import tool_effect
from medmcp_template.tools.example import add_numbers

mcp = FastMCP("medmcp-template")

# Register tools here — one add_tool call per domain tool, each with its effect
# ("read_only", "writes_new" or "destructive"; see effects.py) for the approval card.
mcp.add_tool(add_numbers, **tool_effect("read_only"))
# mcp.add_tool(process_image, **tool_effect("writes_new"))


def server_config() -> dict[str, object]:
    """Return MCP server metadata for autodiscovery by the local agent."""
    return {
        "name": "medmcp-template",
        "command": "medmcp-template",
        "skills_path": str(_pkg_files("medmcp_template") / "skills"),
        "tool_timeout_sec": 300.0,
        # If this stack is slow to start — importing torch, loading weights — set
        # a startup budget too. The agent gives a server only a few seconds to
        # answer "what tools do you have" before giving up, and a stack that
        # misses that window loads with *no* tools and nothing saying why.
        # "startup_timeout_sec": 120.0,
    }


async def _serve(protocol: TextIO) -> None:
    async with stdio_server(stdout=anyio.wrap_file(protocol)) as (read, write):
        server = mcp._mcp_server  # pyright: ignore[reportPrivateUsage]
        await server.run(read, write, server.create_initialization_options())


def main() -> None:
    """Launch the MCP server over stdio (JSON-RPC)."""
    # Worker processes (nnU-Net's preprocessing, PyTorch DataLoader workers) are
    # started fresh, never forked: a forked child inherits stdin's lock while the
    # stdio transport's reader thread holds it, and hangs closing stdin at start.
    multiprocessing.set_start_method("spawn", force=True)
    # JSON-RPC gets its own copy of the agent's pipe; fd 1 itself goes to the log,
    # so what libraries and worker processes print cannot reach the protocol.
    protocol = os.fdopen(os.dup(1), "w", encoding="utf-8")
    sys.stdout.flush()
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    anyio.run(_serve, protocol)
