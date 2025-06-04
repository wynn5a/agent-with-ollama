#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smolagents Agent with Local Ollama Integration

This script demonstrates how to create an AI agent using the smolagents framework
with a local Ollama model (qwen3:latest) and proper handling of thinking tags.
"""

import os
import sys
from dotenv import load_dotenv
from smolagents import CodeAgent

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from qwen_model_wrapper import create_qwen_model

# Load environment variables
load_dotenv()

def create_ollama_agent():
    """
    Create and configure a CodeAgent with local Ollama model.
    
    Returns:
        CodeAgent: Configured agent instance
    """
    # Configure the Qwen model wrapper for Ollama
    model = create_qwen_model(
        model_id="ollama_chat/qwen3:latest",  # Your local Ollama model
        api_base="http://localhost:11434",    # Default Ollama API endpoint
        api_key="dummy_key",                  # Ollama doesn't require API key but LiteLLM expects one
        num_ctx=8192,                         # Context window size - important for agent behavior
        temperature=0.1,                      # Low temperature for more consistent responses
    )
    
    # Create the agent with base tools enabled
    agent = CodeAgent(
        tools=[],                    # Start with empty tools list
        model=model,                 # Use our Qwen model wrapper
        add_base_tools=True,         # Enable built-in tools (calculator, python_code_interpreter, etc.)
    )
    
    return agent

def main():
    """Main function to run the agent."""
    print("🤖 Initializing Smolagents with Local Ollama Model...")
    print("Model: qwen3:latest (with thinking tag filtering)")
    print("Endpoint: http://localhost:11434")
    print("-" * 50)
    
    try:
        # Create the agent
        agent = create_ollama_agent()
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
        print("=" * 50)
        
        # Interactive loop
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print(f"\n🤖 Agent is thinking...")
                
                # Run the agent with user input
                result = agent.run(user_input)
                
                print(f"\n🤖 Agent: {result}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again with a different query.")
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Verify the model is available: ollama list")
        print("3. Pull the model if needed: ollama pull qwen3:latest")

if __name__ == "__main__":
    main() 