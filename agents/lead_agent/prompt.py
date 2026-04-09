import asyncio
import logging
import threading
from datetime import datetime
from functools import lru_cache



logger = logging.getLogger(__name__)

def format_memory_for_injection(memory_data: dict[str, Any], max_tokens: int = 2000) -> str:
    """Format memory data for injection into system prompt.

    Args:
        memory_data: The memory data dictionary.
        max_tokens: Maximum tokens to use (counted via tiktoken for accuracy).

    Returns:
        Formatted memory string for system prompt injection.
    """
    if not memory_data:
        return ""
    
    sections = []

    


def _get_memory_context(agent_name: str | None = None) -> str:
    """Get memory context for injection into system prompt.

    Args:
        agent_name: If provided, loads per-agent memory. If None, loads global memory.

    Returns:
        Formatted memory context string wrapped in XML tags, or empty string if disabled.
    """
    try:
        from agents.memory import format_memory_for_injection, get_memory_data
        from config.memory_config import get_memory_config

        config = get_memory_config()
        if not config.enabled or not config.injection_enabled:
            return ""
        
        memory_data = get_memory_data(agent_name)
        memory_content = format_memory_for_injection(memory_data, max_tokens=config.max_injection_tokens)

        if not memory_content.strip():
            return ""
        
        return f"""<memory>
{memory_content}
</memory>
"""
    
    except Exception as e:
        logger.error("Failed to load memory context: %s", e)
        return ""



def apply_prompt_template(subagent_enabled: bool = False, max_concurrent_subagents: int = 3, *, agent_name: str | None = None, available_skills: set[str] | None = None) -> str:
    # Get memory context
    memory_context = _get_memory_context(agent_name)

    # Include subagent section only if enabled (from runtime parameter)
    n = max_concurrent_subagents
    subagent_section = _build_subagent_section(n) if subagent_enabled else ""

    # Add subagent reminder to critical_reminders if enabled
    # 子代理提醒
    # Orchestrator Mode(任务编排器): 将复杂任务分解为并行子任务
    # HARD LIMIT: 每次响应最多调用 n 次 `task`。如果子任务超过 n 个，分批顺序执行，每批 ≤ n 个。所有批次完成后进行综合。
    subagent_reminder = (
        "- **Orchestrator Mode**: You are a task orchestrator - decompose complex tasks into parallel sub-tasks. "
        f"**HARD LIMIT: max {n} `task` calls per response.** "
        f"If >{n} sub-tasks, split into sequential batches of ≤{n}. Synthesize after ALL batches complete.\n"
        if subagent_enabled
        else ""
    )

    # Add subagent thinking guidance if enabled
    # 子代理思考： 分解检查：此任务是否可以分解为 2 个或更多并行子任务？如果可以，则统计子任务数量
    # 如果子任务数量 > n，则必须计划批次，每批 ≤ n，并且现在只启动第一批。永远不要在一个响应中启动超过 n 个 `task` 调用。
    subagent_thinking = (
        "- **DECOMPOSITION CHECK: Can this task be broken into 2+ parallel sub-tasks? If YES, COUNT them. "
        f"If count > {n}, you MUST plan batches of ≤{n} and only launch the FIRST batch now. "
        f"NEVER launch more than {n} `task` calls in one response.**\n"
        if subagent_enabled
        else ""
    )

    # Get skills section
    skills_section = get_skills_prompt_section(available_skills)

    # Get deferred tools section (tool_search) —— 获取延迟工具部分
    deferred_tools_section = get_deferred_tools_prompt_section()

    # Build ACP agent section only if ACP agents are configured
    acp_section = _build_acp_section()
    custom_mounts_section = _build_custom_mounts_section()
    acp_and_mounts_section = "\n".join(section for section in (acp_section, custom_mounts_section) if section)

    # Format the prompt with dynamic skills and memory
    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        agent_name=agent_name or "DeerFlow 2.0",
        soul=get_agent_soul(agent_name),
        skills_section=skills_section,
        deferred_tools_section=deferred_tools_section,
        memory_context=memory_context,
        subagent_section=subagent_section,
        subagent_reminder=subagent_reminder,
        subagent_thinking=subagent_thinking,
        acp_section=acp_and_mounts_section,
    )

    return prompt + f"\n<current_date>{datetime.now().strftime('%Y-%m-%d, %A')}</current_date>"