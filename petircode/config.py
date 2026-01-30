"""
Configuration management for PetriCode bot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Bot configuration"""

    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

    # Webhook settings
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))

    # Admin users
    ADMIN_USER_IDS = [
        int(uid.strip())
        for uid in os.getenv('ADMIN_USER_IDS', '').split(',')
        if uid.strip()
    ]

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # DeepSeek API settings
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')
    DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

    # Claude API settings
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
    CLAUDE_API_URL = os.getenv('CLAUDE_API_URL', 'https://api.anthropic.com/v1/messages')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
    CLAUDE_TIMEOUT = int(os.getenv('CLAUDE_TIMEOUT', '300'))
    CLAUDE_WORK_DIR = os.getenv('CLAUDE_WORK_DIR', r'C:\workspace\claudecodelabspace')

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        return True


config = Config()
