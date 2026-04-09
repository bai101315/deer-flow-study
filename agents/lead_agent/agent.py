import logging

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, SummarizationMiddleware
from langchain_core.runnables import RunnableConfig


from models.factory import create_chat_model

logger = logging.getLogger(__name__)




def make_lead_agent(config: RunnableConfig):
    cfg = config.get("configurable", {})

    thinking_enabled = cfg.get("thinking_enabled", True)
    reasoning_effort = cfg.get("reasoning_effort", None)
    requested_model_name: str | None = cfg.get("model_name") or cfg.get("model")
    is_plan_mode = cfg.get("is_plan_mode", False)
    subagent_enabled = cfg.get("subagent_enabled", False)
    max_concurrent_subagents = cfg.get("max_concurrent_subagents", 3)
    is_bootstrap = cfg.get("is_bootstrap", False)
    agent_name = cfg.get("agent_name")


    return create_agent(
        model=create_chat_model(name=requested_model_name, thinking_enabled=thinking_enabled),
        system_prompt=apply_prompt_template(
            subagent_enabled=subagent_enabled, max_concurrent_subagents=max_concurrent_subagents, agent_name=agent_name, available_skills=set(agent_config.skills) if agent_config and agent_config.skills is not None else None
        ),
    )


