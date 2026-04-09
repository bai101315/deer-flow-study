import asyncio
import logging

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
from agents.lead_agent.agent import make_lead_agent

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[35m"


async def main():
    config = {
        "configurable":{
            "thread_id": "debug-thread-001",
            "thinking_enabled": True,
            "is_plan_mode": True,
            "model_name": "minimax-m2.7",
            "subagent_enabled": False,
            "tools_enabled": False
        }
    }
    agent = make_lead_agent(config)

    while True:
        try:
             
            user_input = input(f"{CYAN}{BOLD}You >> {RESET}")
            if not user_input:
                continue
            if user_input.lower() in ("q", "exit", ""):
                    print("Goodbye!")
                    break
            
            # Invoke the agent
            state = {"messages": [HumanMessage(content=user_input)]}
            result = await agent.ainvoke(state, config=config, context={"thread_id": "debug-thread-001"})

            # Print the response
            if result.get("messages"):
                last_message = result["messages"][-1]
                print(f"\n{GREEN}{BOLD}Agent{RESET}: {last_message.content}")

        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback

            traceback.print_exc()
        
        

if __name__ == "__main__":
    asyncio.run(main())

