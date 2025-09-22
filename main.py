import json
from claude_client import ClaudeClient
from tools.arxiv_tool import ArxivTool

def tool_router(tool_request: dict):
    """
    Routes tool calls based on Claude's request.
    """
    tool_name = tool_request.get("tool")
    params = tool_request.get("params", {})

    if tool_name == "arxiv":
        query = params.get("query", "")
        max_results = params.get("max_results", 2)
        return ArxivTool.search(query, max_results=max_results)

    return {"error": f"Unknown tool '{tool_name}'"}

if __name__ == "__main__":
    claude = ClaudeClient()

    # Step 1: User sends a high-level request
    user_message = "Find me recent arXiv papers about reinforcement learning in large language models."

    system_prompt = ("You are an AI with access to tools. If you need to search for academic papers, "
                    "respond ONLY in JSON format: {\"tool\": \"arxiv\", \"params\": {\"query\": \"search terms\", \"max_results\": 2}}")

    messages = [
        {"role": "user", "content": user_message}
    ]

    # Step 2: Ask Claude how to handle it
    plan = claude.chat(messages, max_tokens=300, system=system_prompt)

    print("Claude's decision:", plan)

    # Step 3: If Claude outputs a tool request in JSON → call the tool
    try:
        tool_request = json.loads(plan)   # if Claude followed instructions
        tool_result = tool_router(tool_request)

        # Step 4: Give the result back to Claude to summarize
        messages.append({"role": "assistant", "content": plan})
        messages.append({"role": "user", "content": f"Here are the results: {json.dumps(tool_result, indent=2)}. Please summarize the key insights."})

        final_reply = claude.chat(messages, system="You are a helpful research assistant. Summarize academic papers clearly.")
        print("\nClaude's Summary:\n", final_reply)

    except json.JSONDecodeError:
        print("\nClaude replied (not a tool request):\n", plan)