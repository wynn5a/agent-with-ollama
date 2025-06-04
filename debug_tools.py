#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to investigate web search tool issues
"""

import sys
import os
import requests

# Add utils directory to path
sys.path.append('utils')
from qwen_model_wrapper import create_qwen_model
from smolagents import CodeAgent

def test_network_connectivity():
    """Test basic network connectivity."""
    print("🌐 Testing Network Connectivity")
    print("=" * 50)
    
    test_urls = [
        "https://www.google.com",
        "https://httpbin.org/get",
        "https://api.duckduckgo.com",
        "https://www.bing.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {url}: Connection Error")
        except requests.exceptions.Timeout:
            print(f"⏰ {url}: Timeout")
        except Exception as e:
            print(f"❌ {url}: {type(e).__name__}: {e}")

def inspect_web_tools():
    """Inspect the web search tools configuration."""
    print("\n🔍 Inspecting Web Tools")
    print("=" * 50)
    
    try:
        # Create agent
        model = create_qwen_model(verbose=False)
        agent = CodeAgent(tools=[], model=model, add_base_tools=True)
        
        print(f"Total tools available: {len(agent.tools)}")
        print(f"Tools type: {type(agent.tools)}")
        
        # Debug: print what each tool actually is
        if isinstance(agent.tools, dict):
            print("Tools are stored as a dictionary:")
            for name, tool in agent.tools.items():
                print(f"  {name}: {type(tool)}")
        else:
            for i, tool in enumerate(agent.tools):
                print(f"Tool {i}: {type(tool)} - {tool}")
        
        # Find web-related tools
        web_tools = []
        if isinstance(agent.tools, dict):
            for name, tool in agent.tools.items():
                if 'web' in name.lower() or 'search' in name.lower():
                    web_tools.append((name, tool))
        else:
            for tool in agent.tools:
                tool_name = tool if isinstance(tool, str) else getattr(tool, 'name', str(tool))
                if 'web' in tool_name.lower() or 'search' in tool_name.lower():
                    web_tools.append(tool)
        
        print(f"Web-related tools found: {len(web_tools)}")
        
        for item in web_tools:
            if isinstance(item, tuple):
                name, tool = item
                print(f"\n📋 Tool: {name}")
                print(f"   Type: {type(tool)}")
                print(f"   Description: {getattr(tool, 'description', 'No description')}")
                
                # Check if tool has specific attributes
                attrs_to_check = ['api_key', 'base_url', 'endpoint', 'search_engine', 'api_endpoint']
                for attr in attrs_to_check:
                    if hasattr(tool, attr):
                        value = getattr(tool, attr)
                        print(f"   {attr}: {value}")
                
                # Try to inspect the tool's forward method
                if hasattr(tool, 'forward'):
                    import inspect
                    try:
                        signature = inspect.signature(tool.forward)
                        print(f"   Parameters: {list(signature.parameters.keys())}")
                    except:
                        print("   Parameters: Could not inspect")
            else:
                tool = item
                if isinstance(tool, str):
                    print(f"\n📋 Tool: {tool} (string)")
                else:
                    print(f"\n📋 Tool: {getattr(tool, 'name', 'Unknown')}")
                    print(f"   Type: {type(tool)}")
                    print(f"   Description: {getattr(tool, 'description', 'No description')}")
        
        return web_tools
        
    except Exception as e:
        print(f"❌ Error inspecting tools: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_web_search_manually():
    """Test web search functionality manually."""
    print("\n🧪 Testing Web Search Manually")
    print("=" * 50)
    
    try:
        model = create_qwen_model(verbose=False)
        agent = CodeAgent(tools=[], model=model, add_base_tools=True)
        
        print(f"Agent tools type: {type(agent.tools)}")
        
        # Find web search tool
        web_search_tool = None
        if isinstance(agent.tools, dict):
            web_search_tool = agent.tools.get('web_search')
        else:
            for tool in agent.tools:
                tool_name = tool if isinstance(tool, str) else getattr(tool, 'name', str(tool))
                if 'web_search' in tool_name or 'search' in tool_name:
                    web_search_tool = tool
                    break
        
        if not web_search_tool:
            print("❌ No web_search tool found")
            if isinstance(agent.tools, dict):
                print("Available tools:")
                for name in agent.tools.keys():
                    print(f"  - {name}")
            return
        
        print(f"✅ Found search tool: {type(web_search_tool)}")
        
        # Try to call it directly
        try:
            print("🔍 Testing search for 'python programming'...")
            result = web_search_tool.forward("python programming")
            print(f"✅ Search result: {result[:500]}...")
        except Exception as e:
            print(f"❌ Search failed: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error in manual test: {e}")
        import traceback
        traceback.print_exc()

def check_environment_variables():
    """Check for relevant environment variables."""
    print("\n🔧 Checking Environment Variables")
    print("=" * 50)
    
    env_vars_to_check = [
        'SERPER_API_KEY',
        'GOOGLE_API_KEY', 
        'GOOGLE_CSE_ID',
        'BING_API_KEY',
        'SERPAPI_API_KEY',
        'HTTP_PROXY',
        'HTTPS_PROXY',
        'NO_PROXY'
    ]
    
    for var in env_vars_to_check:
        value = os.environ.get(var)
        if value:
            # Mask API keys for security
            if 'key' in var.lower() or 'api' in var.lower():
                masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def main():
    """Run all diagnostic tests."""
    print("🔍 Web Search Tools Diagnostic")
    print("=" * 60)
    
    # Test network connectivity
    test_network_connectivity()
    
    # Check environment variables
    check_environment_variables()
    
    # Inspect web tools
    web_tools = inspect_web_tools()
    
    # Test web search manually
    test_web_search_manually()
    
    print("\n" + "=" * 60)
    print("🏁 Diagnostic Complete")
    
    if not web_tools:
        print("\n💡 Recommendations:")
        print("1. Check if smolagents has web search tools enabled")
        print("2. Verify network connectivity")
        print("3. Check if API keys are required")

if __name__ == "__main__":
    main() 