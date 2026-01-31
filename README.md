# TelegramBotMCP

Telegram Bot MCP Server - 为 Claude Code CLI 提供 Telegram 消息能力

## 功能特性

这是一个 MCP (Model Context Protocol) 服务器，让 Claude Code CLI 可以：
- 发送消息到 Telegram
- 接收 Telegram 消息
- 与 Telegram Bot 交互

## 安装

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 配置环境变量:
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 Telegram Bot Token
```

## 配置到 Claude Code CLI

使用以下命令将此 MCP 服务器添加到 Claude Code CLI：

```bash
claude mcp add telegram-bot -e TELEGRAM_BOT_TOKEN=7871305869:AAECL5dp4eItPvHhiJ9UxEuzPweGKHcXjNM -- python C:\workspace\claudecodelabspace\TelegramBotMCP\mcp_server.py
```

## 可用工具

### 1. send_telegram_message
发送消息到 Telegram 聊天

参数:
- `chat_id`: Telegram 聊天 ID 或用户名 (例如: '@myautomaticagentbot')
- `text`: 要发送的消息文本

### 2. get_telegram_updates
获取最近的 Telegram 消息

参数:
- `limit`: 获取的消息数量 (默认: 10)

## 使用示例

在 Claude Code CLI 中，你可以这样使用：

```
发送消息到我的 Telegram: "Hello from Claude Code!"
```

Claude Code 会自动调用 `send_telegram_message` 工具发送消息。

