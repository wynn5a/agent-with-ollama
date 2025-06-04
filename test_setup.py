#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for Smolagents + Ollama Setup

This script verifies that your Ollama server is running and the smolagents
integration is working correctly.
"""

import requests
import sys
from smolagents import LiteLLMModel, CodeAgent

def test_ollama_connection():
    """Test if Ollama server is accessible."""
    print("🔍 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✅ Ollama server is running!")
            print(f"📋 Available models: {len(models)}")
            
            # Check if qwen3:latest is available
            qwen_models = [m for m in models if 'qwen3' in m.get('name', '').lower()]
            if qwen_models:
                print("✅ Qwen3 model found!")
                for model in qwen_models:
                    print(f"   - {model.get('name', 'Unknown')}")
                return True
            else:
                print("❌ Qwen3 model not found!")
                print("💡 Run: ollama pull qwen3:latest")
                return False
        else:
            print(f"❌ Ollama server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server!")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def test_smolagents_import():
    """Test if smolagents can be imported."""
    print("\n🔍 Testing smolagents import...")
    
    try:
        from smolagents import CodeAgent, LiteLLMModel, Tool
        print("✅ Smolagents imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Failed to import smolagents: {e}")
        print("💡 Run: pip install smolagents[litellm]")
        return False

def test_agent_creation():
    """Test if we can create an agent with Ollama."""
    print("\n🔍 Testing agent creation...")
    
    try:
        model = LiteLLMModel(
            model_id="ollama_chat/qwen3:latest",
            api_base="http://localhost:11434",
            api_key="dummy_key",
            num_ctx=4096,  # Smaller context for testing
            temperature=0.1,
        )
        
        agent = CodeAgent(
            tools=[],
            model=model,
            add_base_tools=True,
        )
        
        print("✅ Agent created successfully!")
        return True, agent
        
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return False, None

def test_simple_query(agent):
    """Test a simple query with the agent."""
    print("\n🔍 Testing simple query...")
    
    try:
        print("🤖 Asking agent: 'What is 2 + 2?'")
        result = agent.run("What is 2 + 2?")
        print(f"✅ Agent responded: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Smolagents + Ollama Setup Test")
    print("=" * 50)
    
    # Test 1: Ollama connection
    ollama_ok = test_ollama_connection()
    
    # Test 2: Smolagents import
    smolagents_ok = test_smolagents_import()
    
    # Test 3: Agent creation
    if ollama_ok and smolagents_ok:
        agent_ok, agent = test_agent_creation()
        
        # Test 4: Simple query
        if agent_ok and agent:
            query_ok = test_simple_query(agent)
        else:
            query_ok = False
    else:
        agent_ok = False
        query_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Ollama Connection: {'✅ PASS' if ollama_ok else '❌ FAIL'}")
    print(f"Smolagents Import: {'✅ PASS' if smolagents_ok else '❌ FAIL'}")
    print(f"Agent Creation:    {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"Simple Query:      {'✅ PASS' if query_ok else '❌ FAIL'}")
    
    if all([ollama_ok, smolagents_ok, agent_ok, query_ok]):
        print("\n🎉 All tests passed! Your setup is ready to use.")
        print("💡 Run 'python main.py' to start the interactive agent.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 