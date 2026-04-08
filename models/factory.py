import logging
import os

from langchain.chat_models import BaseChatModel

logger = logging.getLogger(__name__)



def create_chat_model(name: str | None = None, thinking_enabled: bool = False, **kwargs) -> BaseChatModel:
    """Create a chat model instance from the config.

    Args:
        name: The name of the model to create. If None, the first model in the config will be used.

    Returns:
        A chat model instance.
    """
    model_name = name or "qwen3.5-plus"

    # Use DashScope OpenAI-compatible endpoint for Qwen models.
    base_url = kwargs.pop("base_url", None) or os.getenv("OPENAI_API_BASE") or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    api_key = kwargs.pop("api_key", None) or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY is required to use qwen models.")

    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError("Missing dependency: langchain-openai. Install it before creating chat models.") from exc

    extra_body = dict(kwargs.pop("extra_body", {}) or {})
    if thinking_enabled:
        extra_body["enable_thinking"] = True

    if model_name != "qwen3.5-plus":
        logger.warning("Model '%s' is not explicitly configured; using DashScope-compatible ChatOpenAI init.", model_name)

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        extra_body=extra_body or None,
        **kwargs,
    )
