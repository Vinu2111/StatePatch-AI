from statepatch import AgentTracker, LoopDetector

def main():
    tracker = AgentTracker(agent_name="supply_chain_agent")
    detector = LoopDetector()
    
    stalling_step = None
    diverging_step = None
    
    print("Simulating agent steps...\n")
    
    for i in range(1, 9):
        if i < 5:
            tool_name = f"query_db_table_{i}"
            tool_args = {"table_id": i}
            error = None
        else:
            tool_name = "query_supplier_db"
            tool_args = {"supplier_id": "SUP_404"}
            error = "404 Not Found"
            
        tracker.record_step(
            tool_name=tool_name,
            tool_args=tool_args,
            tool_result="Success" if error is None else "Error",
            token_count=100 + i * 10,
            error=error
        )
        
        steps = tracker.get_steps()
        res = detector.compute_gain(steps)
        
        status = res["status"]
        print(f"Step {i} | Status: {status:15} | Gain: {res['smoothed_gain']:.4f} | Repeats: {res['consecutive_repeats']} | Error Ratio: {res['error_ratio']:.2f}")
        
        if status == "STALLING" and stalling_step is None:
            stalling_step = i
        if status == "DIVERGING" and diverging_step is None:
            diverging_step = i
            
    print("\n--- Summary ---")
    print(f"First STALLING step: {stalling_step}")
    print(f"First DIVERGING step: {diverging_step}")

if __name__ == "__main__":
    main()
