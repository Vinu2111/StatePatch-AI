from typing import List
from .models import StepRecord

class LoopDetector:
    def __init__(self, alpha: float = 0.3, stall_threshold: float = 0.85, diverge_threshold: float = 1.10):
        self.alpha = alpha
        self.stall_threshold = stall_threshold
        self.diverge_threshold = diverge_threshold
        self.previous_smoothed = 0.0

    def compute_gain(self, steps: List[StepRecord]) -> dict:
        step_count = len(steps)
        if step_count < 2:
            return {
                "status": "INSUFFICIENT_DATA",
                "smoothed_gain": 0.0,
                "consecutive_repeats": 0,
                "error_ratio": 0.0,
                "step_count": step_count
            }

        # Count consecutive identical tool_name + tool_args combinations
        # at the end of the steps list
        consecutive_repeats = 0
        last_step = steps[-1]
        
        for step in reversed(steps):
            if step.tool_name == last_step.tool_name and step.tool_args == last_step.tool_args:
                consecutive_repeats += 1
            else:
                break
                
        # Calculate error_ratio
        error_count = sum(1 for step in steps if step.error is not None)
        error_ratio = error_count / step_count
        
        # Calculate a smoothed gain score
        gain = consecutive_repeats / max(step_count, 1)
        smoothed = self.alpha * gain + (1 - self.alpha) * self.previous_smoothed
        self.previous_smoothed = smoothed
        
        # Map smoothed gain to status string
        if smoothed < 0.3:
            status = "FAST_CONVERGE"
        elif 0.3 <= smoothed < self.stall_threshold:
            status = "CONVERGING"
        elif self.stall_threshold <= smoothed < 1.05:
            status = "STALLING"
        elif 1.05 <= smoothed < self.diverge_threshold:
            status = "OSCILLATING"
        else:
            status = "DIVERGING"
            
        return {
            "status": status,
            "smoothed_gain": smoothed,
            "consecutive_repeats": consecutive_repeats,
            "error_ratio": error_ratio,
            "step_count": step_count
        }
