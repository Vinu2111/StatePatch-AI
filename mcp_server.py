import json
from mcp.server.fastmcp import FastMCP
from statepatch import AgentTracker, LoopDetector

SESSIONS = {}

mcp = FastMCP("StatePatch")

@mcp.tool()
def record_step(session_id: str, tool_name: str, tool_args: str, tool_result: str, token_count: int, error: str = "") -> str:
    """Record a single agent step into the StatePatch tracker"""
    if session_id not in SESSIONS:
        SESSIONS[session_id] = AgentTracker(session_id)
        
    tracker = SESSIONS[session_id]
    
    try:
        parsed_args = json.loads(tool_args)
        if not isinstance(parsed_args, dict):
            parsed_args = {"raw": tool_args}
    except json.JSONDecodeError:
        parsed_args = {"raw": tool_args}
        
    actual_error = None if error == "" else error
    
    tracker.record_step(
        tool_name=tool_name,
        tool_args=parsed_args,
        tool_result=tool_result,
        token_count=token_count,
        error=actual_error
    )
    
    n = len(tracker.get_steps())
    return f"Step recorded. Total steps: {n}"

@mcp.tool()
def check_status(session_id: str) -> str:
    """Check the current loop detection status for an agent session"""
    if session_id not in SESSIONS:
        return "Session not found"
        
    tracker = SESSIONS[session_id]
    detector = LoopDetector()
    res = detector.compute_gain(tracker.get_steps())
    
    return (
        f"Status: {res['status']} | Gain: {res['smoothed_gain']:.4f} | "
        f"Repeats: {res['consecutive_repeats']} | "
        f"Error Ratio: {res['error_ratio']:.2f} | "
        f"Steps: {res['step_count']}"
    )

@mcp.tool()
def get_session_summary(session_id: str) -> str:
    """Get a full summary of all steps recorded in a session"""
    if session_id not in SESSIONS:
        return "Session not found"
        
    tracker = SESSIONS[session_id]
    steps = tracker.to_dict()
    total = len(steps)
    
    lines = [f"Session {session_id} — {total} steps total:"]
    for step in steps:
        err_str = step['error'] if step['error'] else 'ok'
        args_str = json.dumps(step['tool_args'])
        lines.append(f"Step {step['step_number']}: {step['tool_name']}({args_str}) -> {step['tool_result']} [{err_str}]")
        
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()
