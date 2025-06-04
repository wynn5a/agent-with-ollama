#!/usr/bin/env python3
"""
Batch Processing Example for Smolagents

This script demonstrates how to process multiple tasks in batch with the smolagents framework.
"""

import json
import time
from datetime import datetime
from smolagents import CodeAgent, LiteLLMModel

def create_agent():
    """Create and configure the agent."""
    model = LiteLLMModel(
        model_id="ollama_chat/qwen3:latest",
        api_base="http://localhost:11434",
        api_key="dummy_key",
        num_ctx=8192,
        temperature=0.1,
    )
    
    agent = CodeAgent(
        tools=[],
        model=model,
        add_base_tools=True,
    )
    
    return agent

def process_tasks_batch(agent, tasks, output_file=None):
    """
    Process a list of tasks in batch mode.
    
    Args:
        agent: The configured CodeAgent
        tasks: List of task strings
        output_file: Optional file to save results
    
    Returns:
        List of results
    """
    results = []
    
    print(f"🔄 Processing {len(tasks)} tasks in batch mode...")
    print("=" * 50)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n📝 Task {i}/{len(tasks)}: {task}")
        
        try:
            start_time = time.time()
            result = agent.run(task)
            end_time = time.time()
            
            task_result = {
                "task_id": i,
                "task": task,
                "result": result,
                "execution_time": round(end_time - start_time, 2),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
            print(f"✅ Completed in {task_result['execution_time']}s")
            print(f"🤖 Result: {result}")
            
        except Exception as e:
            task_result = {
                "task_id": i,
                "task": task,
                "result": None,
                "error": str(e),
                "execution_time": None,
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
            
            print(f"❌ Error: {e}")
        
        results.append(task_result)
        
        # Small delay between tasks to avoid overwhelming the model
        time.sleep(1)
    
    # Save results to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {output_file}")
    
    return results

def generate_summary_report(results):
    """Generate a summary report of batch processing results."""
    total_tasks = len(results)
    successful_tasks = len([r for r in results if r['status'] == 'success'])
    failed_tasks = total_tasks - successful_tasks
    
    if successful_tasks > 0:
        avg_execution_time = sum(r['execution_time'] for r in results if r['execution_time']) / successful_tasks
    else:
        avg_execution_time = 0
    
    print("\n" + "=" * 50)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 50)
    print(f"Total Tasks: {total_tasks}")
    print(f"Successful: {successful_tasks}")
    print(f"Failed: {failed_tasks}")
    print(f"Success Rate: {(successful_tasks/total_tasks)*100:.1f}%")
    print(f"Average Execution Time: {avg_execution_time:.2f}s")
    
    if failed_tasks > 0:
        print("\n❌ Failed Tasks:")
        for result in results:
            if result['status'] == 'error':
                print(f"  - Task {result['task_id']}: {result['task']}")
                print(f"    Error: {result['error']}")

def main():
    """Main function for batch processing demo."""
    print("🔄 Smolagents Batch Processing Demo")
    print("=" * 50)
    
    # Sample tasks for batch processing
    sample_tasks = [
        "Calculate the factorial of 7",
        "What is the square root of 256?",
        "Generate the first 8 prime numbers",
        "Convert 100 degrees Fahrenheit to Celsius",
        "Write a Python function to check if a number is palindrome",
        "Calculate the area of a circle with radius 5",
        "Find the greatest common divisor of 48 and 18",
        "Generate a random password with 12 characters",
        "Calculate compound interest: principal=1000, rate=5%, time=3 years",
        "Sort this list in descending order: [64, 34, 25, 12, 22, 11, 90]"
    ]
    
    try:
        # Create agent
        agent = create_agent()
        print("✅ Agent initialized successfully!")
        
        # Process tasks
        results = process_tasks_batch(
            agent=agent,
            tasks=sample_tasks,
            output_file=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        # Generate summary
        generate_summary_report(results)
        
        # Interactive mode for custom batch
        print("\n" + "=" * 50)
        print("💬 Custom Batch Mode")
        print("Enter tasks one by one (empty line to start processing, 'quit' to exit)")
        print("=" * 50)
        
        custom_tasks = []
        while True:
            task = input(f"\nTask {len(custom_tasks) + 1}: ").strip()
            
            if task.lower() == 'quit':
                break
            elif task == '':
                if custom_tasks:
                    print(f"\n🚀 Starting batch processing of {len(custom_tasks)} custom tasks...")
                    custom_results = process_tasks_batch(
                        agent=agent,
                        tasks=custom_tasks,
                        output_file=f"custom_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    )
                    generate_summary_report(custom_results)
                    custom_tasks = []
                else:
                    print("No tasks to process.")
            else:
                custom_tasks.append(task)
                print(f"✅ Added task: {task}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 