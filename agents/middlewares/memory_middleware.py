"""Middleware for memory mechanism.
gentState（Agent 状态基类）、AgentMiddleware（中间件基类）、Runtime（运行时上下文）、get_config（配置获取）；
内存队列（get_memory_queue）、内存配置（get_memory_config）
"""

import logging
import re
from typing import Any, override

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langgraph.config import get_config
from langgraph.runtime import Runtime

from agents.memory.queue import get_memory_queue
from config.memory_config import get_memory_config

logger = logging.getLogger(__name__)

# 匹配 <uploaded_files> 块，移除临时的文件上传信息（不持久化到长期记忆）
_UPLOAD_BLOCK_RE = re.compile(r"<uploaded_files>[\s\S]*?</uploaded_files>\n*", re.IGNORECASE)

# 纠正信号（用户明确表示之前的回答 / 行动有误，需要改正）
_CORRECTION_PATTERNS = (
    re.compile(r"\bthat(?:'s| is) (?:wrong|incorrect)\b", re.IGNORECASE),
    re.compile(r"\byou misunderstood\b", re.IGNORECASE),
    re.compile(r"\btry again\b", re.IGNORECASE),
    re.compile(r"\bredo\b", re.IGNORECASE),
    re.compile(r"不对"),
    re.compile(r"你理解错了"),
    re.compile(r"你理解有误"),
    re.compile(r"重试"),
    re.compile(r"重新来"),
    re.compile(r"换一种"),
    re.compile(r"改用"),
)

_REINFORCEMENT_PATTERNS = (
    re.compile(r"\byes[,.]?\s+(?:exactly|perfect|that(?:'s| is) (?:right|correct|it))\b", re.IGNORECASE),
    re.compile(r"\bperfect(?:[.!?]|$)", re.IGNORECASE),
    re.compile(r"\bexactly\s+(?:right|correct)\b", re.IGNORECASE),
    re.compile(r"\bthat(?:'s| is)\s+(?:exactly\s+)?(?:right|correct|what i (?:wanted|needed|meant))\b", re.IGNORECASE),
    re.compile(r"\bkeep\s+(?:doing\s+)?that\b", re.IGNORECASE),
    re.compile(r"\bjust\s+(?:like\s+)?(?:that|this)\b", re.IGNORECASE),
    re.compile(r"\bthis is (?:great|helpful)\b(?:[.!?]|$)", re.IGNORECASE),
    re.compile(r"\bthis is what i wanted\b(?:[.!?]|$)", re.IGNORECASE),
    re.compile(r"对[，,]?\s*就是这样(?:[。！？!?.]|$)"),
    re.compile(r"完全正确(?:[。！？!?.]|$)"),
    re.compile(r"(?:对[，,]?\s*)?就是这个意思(?:[。！？!?.]|$)"),
    re.compile(r"正是我想要的(?:[。！？!?.]|$)"),
    re.compile(r"继续保持(?:[。！？!?.]|$)"),
)

def _extract_message_text(message: Any) -> str:
    """Extract plain text from message content for filtering and signal detection.
    从消息对象中提取纯文本（兼容多格式 content），为后续过滤 / 信号检测做准备。
    """
    content = getattr(message, "content", "")
    if isinstance(content, list):
        text_parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif isinstance(part, dict):
                text_val = part.get("text")
                if isinstance(text_val, str):
                    text_parts.append(text_val)
        return " ".join(text_parts)
    return str(content)

def detect_reinforcement(messages: list[Any]) -> bool:
    """Detect explicit positive reinforcement signals in recent conversation turns.
    检测最近的用户消息中是否有「正向强化信号」（仅在无修正信号时生效）。
    Complements detect_correction() by identifying when the user confirms the
    agent's approach was correct. This allows the memory system to record what
    worked well, not just what went wrong.

    The queue keeps only one pending context per thread, so callers pass the
    latest filtered message list. Checking only recent user turns keeps signal
    detection conservative while avoiding stale signals from long histories.
    """
    recent_user_msgs = [msg for msg in messages[-6:] if getattr(msg, "type", None) == "human"]

    for msg in recent_user_msgs:
        content = _extract_message_text(msg).strip()
        if not content:
            continue
        if any(pattern.search(content) for pattern in _REINFORCEMENT_PATTERNS):
            return True

    return False

def detect_correction(messages: list[Any]) -> bool:
    """Detect explicit user corrections in recent conversation turns.
    检测最近的用户消息中是否有「修正信号」
    The queue keeps only one pending context per thread, so callers pass the
    latest filtered message list. Checking only recent user turns keeps signal
    detection conservative while avoiding stale corrections from long histories.
    """
    recent_user_msgs = [msg for msg in messages[-6:] if getattr(msg, "type", None) == "human"]

    for msg in recent_user_msgs:
        content = _extract_message_text(msg).strip()
        if not content:
            continue
        if any(pattern.search(content) for pattern in _CORRECTION_PATTERNS):
            return True

    return False

