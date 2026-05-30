# StatePatch

StatePatch is a lightweight Python package for tracking and analyzing the execution steps of agentic workflows. It provides an `AgentTracker` to record individual tool invocations and their outcomes, and a `LoopDetector` to analyze these steps for potential stalling or diverging behavior based on repeating patterns and error rates. The library helps identify when agents get stuck in repetitive loops without making progress, allowing developers to implement automatic recovery strategies.
