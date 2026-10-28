import os
from dotenv import load_dotenv
import anthropic
from prompts import SYSTEM_PROMPT
from tools import TOOL_DEFINITIONS, execute_tool

load_dotenv()
client = anthropic.Anthropic()

MAX_ITERATIONS = 10  # Safety cap — never loop forever

def run_agent(question: str, on_log=None) -> str:
    """
    on_log: optional callable(str) — called with progress messages.
    The agent doesn't know or care what on_log does.
    The UI will pass in a function that emits a Qt signal.
    """
    def log(msg):
        if on_log:
            on_log(msg)
        print(msg)  # always print to terminal too

    log(f"Starting task: {question}")
    messages = [{"role": "user", "content": question}]
    iterations = 0

    while iterations < MAX_ITERATIONS:
        iterations += 1
        log(f"── Iteration {iterations} ──────────────────")

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=messages
        )

        log(f"Stop reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    log("Done — writing answer.")
                    return block.text
            return "Agent finished but produced no text."

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    log(f"Calling tool: {block.name}")
                    log(f"  Input: {block.input}")
                    result = execute_tool(block.name, block.input)
                    log(f"  Result preview: {result[:120]}...")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})
        else:
            return f"Unexpected stop: {response.stop_reason}"

    return f"Hit max iterations ({MAX_ITERATIONS})."

if __name__ == "__main__":
    answer = run_agent("What are the main causes of the 2008 financial crisis?")
    print("\n── ANSWER ──────────────────────────────")
    print(answer)

    import time

def run_agent_safe(question: str) -> dict:
    """
    Wrapper that catches errors and returns structured output.
    Use this in any real application.
    """
    start = time.time()
    
    try:
        answer = run_agent(question)
        return {
            "success": True,
            "answer": answer,
            "duration_seconds": round(time.time() - start, 2)
        }
    except anthropic.APIConnectionError:
        return {"success": False, "error": "Could not reach Anthropic API"}
    except anthropic.RateLimitError:
        return {"success": False, "error": "Rate limit hit — slow down requests"}
    except anthropic.APIStatusError as e:
        return {"success": False, "error": f"API error {e.status_code}: {e.message}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}