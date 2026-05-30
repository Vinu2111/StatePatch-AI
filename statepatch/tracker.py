import time
from typing import List, Dict, Any, Optional
import dataclasses
from .models import StepRecord

class AgentTracker:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.steps: List[StepRecord] = []

    def record_step(self, tool_name: str, tool_args: dict, tool_result: str, token_count: int, error: Optional[str] = None):
        step_number = len(self.steps) + 1
        step = StepRecord(
            step_number=step_number,
            tool_name=tool_name,
            tool_args=tool_args,
            tool_result=tool_result,
            token_count=token_count,
            timestamp=time.time(),
            error=error
        )
        self.steps.append(step)
        return step

    def get_steps(self) -> List[StepRecord]:
        return self.steps

    def to_dict(self) -> List[Dict[str, Any]]:
        return [dataclasses.asdict(step) for step in self.steps]
