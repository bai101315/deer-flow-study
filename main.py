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
from agents.memory import get_memory_queue
from agents.middlewares.memory_middleware import detect_correction, detect_reinforcement

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
    
    # Get the memory queue for automatic memory updates
    memory_queue = get_memory_queue()

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
            
            # ===== NEW: Queue memory update =====
            # After agent completes, queue the conversation for memory update
            messages = result.get("messages", [])
            
            # Detect signals
            correction_detected = detect_correction(messages)
            reinforcement_detected = detect_reinforcement(messages)
            
            # Add to memory queue (will be processed after debounce timeout)
            thread_id = config["configurable"].get("thread_id", "default-thread")
            memory_queue.add(
                thread_id=thread_id,
                messages=messages,
                agent_name=None,  # global memory
                correction_detected=correction_detected,
                reinforcement_detected=reinforcement_detected,
            )
            
            if correction_detected:
                print(f"{YELLOW}[Memory] 检测到修正信号，将更新内存{RESET}")
            elif reinforcement_detected:
                print(f"{YELLOW}[Memory] 检测到正向反馈，将更新内存{RESET}")
            else:
                print(f"{DIM}[Memory] 对话已加入队列，将在30秒后处理{RESET}")
            # ===== END: Memory queue integration =====

        except KeyboardInterrupt:
            print("\nInterrupted. Waiting for memory queue to finish...")
            # Give the memory queue time to process pending updates
            memory_queue.wait_for_processing(timeout=10)
            print("Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback

            traceback.print_exc()
        
        

if __name__ == "__main__":
    asyncio.run(main())

