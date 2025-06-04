#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smolagents Agent with Local Ollama Integration

This script demonstrates how to create an AI agent using the smolagents framework
with a local Ollama model (qwen3:latest) and proper handling of thinking tags.
"""

import os
import sys
import time
from dotenv import load_dotenv
from smolagents import CodeAgent

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from qwen_model_wrapper import create_qwen_model

# Load environment variables
load_dotenv()

def create_ollama_agent(verbose=True):
    """
    Create and configure a CodeAgent with local Ollama model.
    
    Args:
        verbose: Enable verbose logging
    
    Returns:
        CodeAgent: Configured agent instance
    """
    print("🔧 Creating Qwen model wrapper...")
    
    # Configure the Qwen model wrapper for Ollama
    model = create_qwen_model(
        model_id="ollama_chat/qwen3:latest",  # Your local Ollama model
        api_base="http://localhost:11434",    # Default Ollama API endpoint
        api_key="dummy_key",                  # Ollama doesn't require API key but LiteLLM expects one
        num_ctx=8192,                         # Context window size - important for agent behavior
        temperature=0.1,                      # Low temperature for more consistent responses
        verbose=verbose,                      # Enable detailed logging
    )
    
    print("🤖 Creating CodeAgent...")
    
    # Create the agent with base tools enabled
    agent = CodeAgent(
        tools=[],                    # Start with empty tools list
        model=model,                 # Use our Qwen model wrapper
        add_base_tools=True,         # Enable built-in tools (calculator, python_code_interpreter, etc.)
    )
    
    # Print available tools
    if verbose:
        print("\n📋 Available Tools:")
        if hasattr(agent, 'tools') and agent.tools:
            for tool in agent.tools:
                tool_name = getattr(tool, 'name', str(tool))
                tool_desc = getattr(tool, 'description', 'No description')
                print(f"  - {tool_name}: {tool_desc[:100]}...")
        else:
            print("  - No tools found or tools not yet initialized")
    
    return agent

def run_agent_with_logging(agent, query, verbose=True):
    """
    Run the agent with detailed logging.
    
    Args:
        agent: The CodeAgent instance
        query: User query to process
        verbose: Enable verbose logging
        
    Returns:
        Agent response
    """
    if verbose:
        print(f"\n{'='*80}")
        print(f"🚀 STARTING AGENT EXECUTION")
        print(f"{'='*80}")
        print(f"Query: {query}")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # Run the agent
        result = agent.run(query)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"✅ AGENT EXECUTION COMPLETED")
            print(f"{'='*80}")
            print(f"Execution time: {execution_time:.2f} seconds")
            print(f"Final result: {result}")
            print(f"{'='*80}")
        
        return result
        
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"❌ AGENT EXECUTION FAILED")
            print(f"{'='*80}")
            print(f"Execution time: {execution_time:.2f} seconds")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"{'='*80}")
        
        raise e

def main():
    """Main function to run the agent."""
    print("🤖 Initializing Smolagents with Local Ollama Model...")
    print("Model: qwen3:latest (with thinking tag filtering)")
    print("Endpoint: http://localhost:11434")
    print("-" * 50)
    
    # Ask user for verbosity preference
    verbose_input = input("Enable verbose logging? (y/N): ").strip().lower()
    verbose = verbose_input in ['y', 'yes', '1', 'true']
    
    if verbose:
        print("🔍 Verbose logging enabled - you'll see detailed LLM interactions")
    else:
        print("🔇 Quiet mode - minimal logging")
    
    try:
        # Create the agent
        agent = create_ollama_agent(verbose=verbose)
        print("✅ Agent initialized successfully!")
        
        # Example tasks to demonstrate the agent's capabilities
        example_tasks = [
            "Calculate the 10th Fibonacci number",
            "What is the square root of 144?",
            "Write a Python function to reverse a string and test it with 'hello world'",
            "Generate a random number between 1 and 100 and tell me if it's even or odd"
        ]
        
        print("\n🎯 Example tasks you can try:")
        for i, task in enumerate(example_tasks, 1):
            print(f"{i}. {task}")
        
        print("\n" + "=" * 50)
        print("💬 Interactive Mode - Type 'quit' to exit")
        print("💡 Type 'verbose on/off' to toggle detailed logging")
        print("=" * 50)
        
        # Interactive loop
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'verbose on':
                    verbose = True
                    agent.model.verbose = True
                    print("🔍 Verbose logging enabled")
                    continue
                    
                if user_input.lower() == 'verbose off':
                    verbose = False
                    agent.model.verbose = False
                    print("🔇 Verbose logging disabled")
                    continue
                
                if not user_input:
                    continue
                
                print(f"\n🤖 Agent is thinking...")
                
                # Run the agent with detailed logging
                result = run_agent_with_logging(agent, user_input, verbose=verbose)
                
                if not verbose:
                    print(f"\n🤖 Agent: {result}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                if verbose:
                    import traceback
                    print("📋 Full traceback:")
                    traceback.print_exc()
                print("Please try again with a different query.")
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Verify the model is available: ollama list")
        print("3. Pull the model if needed: ollama pull qwen3:latest")

if __name__ == "__main__":
    main() 