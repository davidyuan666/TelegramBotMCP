#!/usr/bin/env python3
"""
Telegram Bot MCP Server
Provides Telegram messaging capabilities to Claude Code CLI via MCP
"""
import asyncio
import logging
import os
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from telegram import Bot
from telegram.error import TelegramError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("telegram-bot")

# Telegram bot instance
bot: Bot | None = None


def get_bot() -> Bot:
    """Get or create Telegram bot instance"""
    global bot
    if bot is None:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        bot = Bot(token=token)
    return bot


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Telegram tools"""
    return [
        Tool(
            name="send_telegram_message",
            description="Send a message to a Telegram chat",
            inputSchema={
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "Telegram chat ID or username (e.g., '@myautomaticagentbot')"
                    },
                    "text": {
                        "type": "string",
                        "description": "Message text to send"
                    }
                },
                "required": ["chat_id", "text"]
            }
        ),
        Tool(
            name="get_telegram_updates",
            description="Get recent messages from Telegram bot",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Number of updates to retrieve (default: 10)",
                        "default": 10
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "send_telegram_message":
            return await send_message(arguments)
        elif name == "get_telegram_updates":
            return await get_updates(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def send_message(arguments: dict) -> list[TextContent]:
    """Send a message to Telegram"""
    chat_id = arguments.get("chat_id")
    text = arguments.get("text")

    if not chat_id or not text:
        return [TextContent(type="text", text="Error: chat_id and text are required")]

    try:
        telegram_bot = get_bot()
        message = await telegram_bot.send_message(chat_id=chat_id, text=text)

        result = f"Message sent successfully!\nChat ID: {message.chat_id}\nMessage ID: {message.message_id}"
        return [TextContent(type="text", text=result)]
    except TelegramError as e:
        return [TextContent(type="text", text=f"Telegram error: {str(e)}")]


async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())


async def get_updates(arguments: dict) -> list[TextContent]:
    """Get recent updates from Telegram"""
    limit = arguments.get("limit", 10)

    try:
        telegram_bot = get_bot()
        updates = await telegram_bot.get_updates(limit=limit)

        if not updates:
            return [TextContent(type="text", text="No recent messages")]

        result = "Recent messages:\n\n"
        for update in updates[-limit:]:
            if update.message:
                msg = update.message
                result += f"From: {msg.from_user.first_name} (@{msg.from_user.username})\n"
                result += f"Chat ID: {msg.chat_id}\n"
                result += f"Text: {msg.text}\n"
                result += f"Date: {msg.date}\n\n"

        return [TextContent(type="text", text=result)]
    except TelegramError as e:
        return [TextContent(type="text", text=f"Telegram error: {str(e)}")]


async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
