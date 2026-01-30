"""
Claude API service for computer operations
"""
import logging
import aiohttp
from ..config import config

logger = logging.getLogger(__name__)


async def execute_claude_code(operation: str, timeout: int = None) -> dict:
    """
    Execute computer operation via Claude API with computer use tool

    Args:
        operation: The operation description to execute
        timeout: Timeout in seconds (default: from config)

    Returns:
        dict with keys:
            - stdout: Standard output
            - stderr: Standard error
            - return_code: Process return code
            - success: Boolean indicating success

    Raises:
        Exception: If execution fails
    """
    if timeout is None:
        timeout = config.CLAUDE_TIMEOUT

    if not config.CLAUDE_API_KEY:
        raise ValueError("CLAUDE_API_KEY is not configured")

    logger.info(f"Executing operation via Claude API: {operation}")
    logger.info(f"Working directory: {config.CLAUDE_WORK_DIR}")

    headers = {
        "x-api-key": config.CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # Build request payload with computer use tool
    payload = {
        "model": config.CLAUDE_MODEL,
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": f"Please execute this operation in the directory {config.CLAUDE_WORK_DIR}: {operation}"
            }
        ],
        "tools": [
            {
                "type": "computer_20241022",
                "name": "computer",
                "display_width_px": 1024,
                "display_height_px": 768,
                "display_number": 1
            },
            {
                "type": "bash_20241022",
                "name": "bash"
            }
        ]
    }

    try:
        client_timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            async with session.post(
                config.CLAUDE_API_URL,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Claude API error: {response.status} - {error_text}")
                    raise Exception(f"API returned status {response.status}: {error_text}")

                data = await response.json()
                logger.info(f"API response received")

                # Extract result from response
                result_text = _extract_result_from_response(data)

                return {
                    'stdout': result_text,
                    'stderr': '',
                    'return_code': 0,
                    'success': True
                }

    except aiohttp.ClientError as e:
        logger.error(f"Network error calling Claude API: {e}", exc_info=True)
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Error executing via Claude API: {e}", exc_info=True)
        raise


def _extract_result_from_response(data: dict) -> str:
    """
    Extract result text from Claude API response

    Args:
        data: API response data

    Returns:
        Extracted result text
    """
    try:
        # Extract content from response
        if "content" in data and len(data["content"]) > 0:
            result_parts = []
            for content_block in data["content"]:
                if content_block.get("type") == "text":
                    result_parts.append(content_block.get("text", ""))
                elif content_block.get("type") == "tool_use":
                    # Extract tool result if available
                    tool_result = content_block.get("content", "")
                    if tool_result:
                        result_parts.append(str(tool_result))

            return "\n".join(result_parts) if result_parts else "Operation completed"
        else:
            return "No response content"

    except Exception as e:
        logger.error(f"Error extracting result: {e}")
        return f"Error parsing response: {str(e)}"

