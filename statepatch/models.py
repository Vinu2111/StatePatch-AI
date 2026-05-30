from dataclasses import dataclass
from typing import Optional

@dataclass
class StepRecord:
    step_number: int
    tool_name: str
    tool_args: dict
    tool_result: str
    token_count: int
    timestamp: float
    error: Optional[str] = None
