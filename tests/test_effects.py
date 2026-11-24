"""Tool effects reach an MCP client as ``_meta`` and the standard annotations."""

import sys
from typing import Any, cast

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import Tool, ToolAnnotations

from medmcp_template.effects import EFFECT_META_KEY, Effect, tool_effect

# A server with one tool per level and one without a declaration, served the way
# the template's main() serves its own tools.
_LEVELS_SERVER = """
from mcp.server.fastmcp import FastMCP
from medmcp_template import server
from medmcp_template.effects import tool_effect

def reads() -> str:
    return ""

def writes() -> str:
    return ""

def deletes() -> str:
    return ""

def untagged() -> str:
    return ""

server.mcp = FastMCP("levels")
server.mcp.add_tool(reads, **tool_effect("read_only"))
server.mcp.add_tool(writes, **tool_effect("writes_new"))
server.mcp.add_tool(deletes, **tool_effect("destructive"))
server.mcp.add_tool(untagged)
server.main()
"""

_TEMPLATE_SERVER = "from medmcp_template.server import main; main()"


async def _list_tools(code: str) -> dict[str, Tool]:
    params = StdioServerParameters(command=sys.executable, args=["-c", code])
    async with (
        stdio_client(params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        result = await session.list_tools()
    return {tool.name: tool for tool in result.tools}


@pytest.mark.parametrize(
    ("effect", "read_only", "destructive"),
    [
        ("read_only", True, False),
        ("writes_new", False, False),
        ("destructive", False, True),
    ],
)
def test_each_level_gives_exact_kwargs(effect: Effect, read_only: bool, destructive: bool) -> None:
    """Each level maps to its ``_meta`` entry and the matching MCP hints, nothing more."""
    kwargs = tool_effect(effect)
    assert kwargs == {
        "annotations": ToolAnnotations(readOnlyHint=read_only, destructiveHint=destructive),
        "meta": {EFFECT_META_KEY: effect},
    }
    assert kwargs["annotations"].idempotentHint is None
    assert kwargs["annotations"].openWorldHint is None


def test_unknown_level_raises_at_registration() -> None:
    """A typo fails where the tool is registered, not when it is called."""
    with pytest.raises(ValueError, match="writes_new"):
        tool_effect(cast(Any, "write_new"))


def test_calls_do_not_share_meta() -> None:
    """Each registration gets its own ``meta`` dict."""
    first = tool_effect("read_only")
    first["meta"]["other"] = 1
    assert tool_effect("read_only")["meta"] == {EFFECT_META_KEY: "read_only"}


async def test_levels_reach_the_client_over_stdio() -> None:
    """``tools/list`` carries the effect and hints for each level, and none when untagged."""
    tools = await _list_tools(_LEVELS_SERVER)

    expected = {
        "reads": ("read_only", True, False),
        "writes": ("writes_new", False, False),
        "deletes": ("destructive", False, True),
    }
    for name, (effect, read_only, destructive) in expected.items():
        tool = tools[name]
        assert tool.meta == {EFFECT_META_KEY: effect}, name
        assert tool.annotations is not None, name
        assert tool.annotations.readOnlyHint is read_only, name
        assert tool.annotations.destructiveHint is destructive, name

    assert tools["untagged"].meta is None
    assert tools["untagged"].annotations is None


async def test_template_example_tool_is_read_only() -> None:
    """The template's own server declares ``add_numbers`` read-only."""
    tools = await _list_tools(_TEMPLATE_SERVER)
    tool = tools["add_numbers"]
    assert tool.meta == {EFFECT_META_KEY: "read_only"}
    assert tool.annotations is not None
    assert tool.annotations.readOnlyHint is True
    assert tool.annotations.destructiveHint is False
