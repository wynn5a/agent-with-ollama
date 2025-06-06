#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Processing Example for Smolagents

This script demonstrates how to process multiple tasks in batch with the smolagents framework.
"""

import json
import time
import sys
import os
from datetime import datetime
from smolagents import CodeAgent

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from qwen_model_wrapper import create_qwen_model

def create_agent(include_code_interpreter=True):
    """Create and configure the agent."""
    model = create_qwen_model(
        model_id="ollama_chat/qwen3:latest",
        api_base="http://localhost:11434",
        api_key="dummy_key",
        num_ctx=8192,
        temperature=0.1,
        verbose=False,  # Disable verbose for batch processing
    )
    
    if include_code_interpreter:
        # Standard agent with all tools
        agent = CodeAgent(
            tools=[],
            model=model,
            add_base_tools=True,
        )
    else:
        # Agent without python code interpreter for code generation tasks
        from smolagents import Tool
        
        # Create a custom agent with only specific tools
        agent = CodeAgent(
            tools=[],
            model=model,
            add_base_tools=False,  # Don't add all base tools
        )
        
        # Manually add only the tools we want (excluding python_code_interpreter)
        from smolagents.default_tools import (
            FinalAnswerTool,
            # We'll skip PythonCodeInterpreterTool for code generation tasks
        )
        
        agent.tools = {
            'final_answer': FinalAnswerTool(),
        }
    
    return agent

def is_code_generation_task(task):
    """
    Determine if a task is asking for code generation vs code execution.
    
    Args:
        task: The task string
        
    Returns:
        bool: True if it's a code generation task
    """
    code_generation_keywords = [
        'write a function',
        'create a function', 
        'show me the code',
        'python function',
        'function that',
        'function to',
        'write code',
        'create code',
        'show code'
    ]
    
    task_lower = task.lower()
    return any(keyword in task_lower for keyword in code_generation_keywords)

def process_tasks_batch(agent, tasks, output_file=None, max_retries=2, timeout_per_task=120):
    """
    Process a list of tasks in batch mode.
    
    Args:
        agent: The configured CodeAgent
        tasks: List of task strings
        output_file: Optional file to save results
        max_retries: Maximum number of retries per task
        timeout_per_task: Maximum time per task in seconds
    
    Returns:
        List of results
    """
    results = []
    
    print(f"🔄 Processing {len(tasks)} tasks in batch mode...")
    print(f"⚙️  Max retries per task: {max_retries}")
    print(f"⏱️  Timeout per task: {timeout_per_task}s")
    print("=" * 50)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n📝 Task {i}/{len(tasks)}: {task}")
        
        # Determine if we need a special agent for this task
        if is_code_generation_task(task):
            print("🔧 Detected code generation task - using agent without code interpreter")
            current_agent = create_agent(include_code_interpreter=False)
            # Modify the task to be more explicit
            modified_task = f"Please provide the Python code for: {task}. Return only the code without executing it."
        else:
            print("🔧 Using standard agent with all tools")
            current_agent = agent
            modified_task = task
        
        retry_count = 0
        task_completed = False
        
        while retry_count <= max_retries and not task_completed:
            try:
                if retry_count > 0:
                    print(f"🔄 Retry {retry_count}/{max_retries}")
                
                start_time = time.time()
                
                # Use the appropriate agent and task
                result = current_agent.run(modified_task)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Check if execution took too long
                if execution_time > timeout_per_task:
                    raise TimeoutError(f"Task exceeded {timeout_per_task}s timeout")
                
                task_result = {
                    "task_id": i,
                    "task": task,  # Store original task
                    "modified_task": modified_task,  # Store modified task
                    "result": result,
                    "execution_time": round(execution_time, 2),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "retries": retry_count,
                    "agent_type": "code_generation" if is_code_generation_task(task) else "standard"
                }
                
                print(f"✅ Completed in {task_result['execution_time']}s")
                print(f"🤖 Result: {result}")
                task_completed = True
                
            except KeyboardInterrupt:
                print("\n⚠️  Batch processing interrupted by user")
                task_result = {
                    "task_id": i,
                    "task": task,
                    "modified_task": modified_task,
                    "result": None,
                    "error": "Interrupted by user",
                    "execution_time": None,
                    "timestamp": datetime.now().isoformat(),
                    "status": "interrupted",
                    "retries": retry_count,
                    "agent_type": "code_generation" if is_code_generation_task(task) else "standard"
                }
                task_completed = True
                
            except Exception as e:
                retry_count += 1
                error_msg = str(e)
                
                print(f"❌ Error: {error_msg}")
                
                if retry_count > max_retries:
                    task_result = {
                        "task_id": i,
                        "task": task,
                        "modified_task": modified_task,
                        "result": None,
                        "error": error_msg,
                        "execution_time": None,
                        "timestamp": datetime.now().isoformat(),
                        "status": "failed",
                        "retries": retry_count - 1,
                        "agent_type": "code_generation" if is_code_generation_task(task) else "standard"
                    }
                    task_completed = True
                    print(f"💀 Task failed after {max_retries} retries")
                else:
                    print(f"🔄 Will retry in 2 seconds...")
                    time.sleep(2)
        
        results.append(task_result)
        
        # Small delay between tasks to avoid overwhelming the model
        if i < len(tasks):  # Don't sleep after the last task
            time.sleep(1)
    
    # Save results to file if specified
    if output_file:
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to {output_file}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")
    
    return results

def generate_summary_report(results):
    """Generate a summary report of batch processing results."""
    total_tasks = len(results)
    successful_tasks = len([r for r in results if r['status'] == 'success'])
    failed_tasks = len([r for r in results if r['status'] == 'failed'])
    interrupted_tasks = len([r for r in results if r['status'] == 'interrupted'])
    
    if successful_tasks > 0:
        avg_execution_time = sum(r['execution_time'] for r in results if r['execution_time']) / successful_tasks
        total_retries = sum(r.get('retries', 0) for r in results if r['status'] == 'success')
    else:
        avg_execution_time = 0
        total_retries = 0
    
    print("\n" + "=" * 50)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 50)
    print(f"Total Tasks: {total_tasks}")
    print(f"Successful: {successful_tasks}")
    print(f"Failed: {failed_tasks}")
    print(f"Interrupted: {interrupted_tasks}")
    print(f"Success Rate: {(successful_tasks/total_tasks)*100:.1f}%")
    print(f"Average Execution Time: {avg_execution_time:.2f}s")
    print(f"Total Retries: {total_retries}")
    
    if failed_tasks > 0:
        print("\n❌ Failed Tasks:")
        for result in results:
            if result['status'] == 'failed':
                retries = result.get('retries', 0)
                print(f"  - Task {result['task_id']}: {result['task']}")
                print(f"    Error: {result['error']}")
                print(f"    Retries: {retries}")
    
    if interrupted_tasks > 0:
        print("\n⚠️  Interrupted Tasks:")
        for result in results:
            if result['status'] == 'interrupted':
                print(f"  - Task {result['task_id']}: {result['task']}")
    
    # Show tasks that required retries
    retry_tasks = [r for r in results if r.get('retries', 0) > 0 and r['status'] == 'success']
    if retry_tasks:
        print("\n🔄 Tasks that required retries:")
        for result in retry_tasks:
            print(f"  - Task {result['task_id']}: {result['task']} ({result['retries']} retries)")

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
        agent = create_agent()  # This will create the standard agent with all tools
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