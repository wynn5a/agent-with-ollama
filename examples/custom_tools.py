#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Tools Example for Smolagents

This script demonstrates how to create and use custom tools with the smolagents framework.
"""

import requests
import json
import sys
import os
from smolagents import Tool, CodeAgent

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from qwen_model_wrapper import create_qwen_model

class WeatherTool(Tool):
    """Custom tool to get weather information."""
    
    name = "weather_checker"
    description = """
    This tool gets current weather information for a given city.
    It returns temperature, humidity, and weather conditions.
    """
    inputs = {
        "city": {
            "type": "string", 
            "description": "The name of the city to get weather for"
        }
    }
    output_type = "string"
    
    def forward(self, city: str) -> str:
        """Get weather information for the specified city."""
        try:
            # Using a free weather API (OpenWeatherMap requires API key in real usage)
            # For demo purposes, we'll return mock data
            mock_weather_data = {
                "temperature": "22°C",
                "humidity": "65%",
                "conditions": "Partly cloudy",
                "wind_speed": "10 km/h"
            }
            
            return f"Weather in {city}: {mock_weather_data['temperature']}, {mock_weather_data['conditions']}, Humidity: {mock_weather_data['humidity']}, Wind: {mock_weather_data['wind_speed']}"
        except Exception as e:
            return f"Sorry, I couldn't get weather information for {city}. Error: {str(e)}"

class TextAnalysisTool(Tool):
    """Custom tool for basic text analysis."""
    
    name = "text_analyzer"
    description = """
    This tool analyzes text and provides statistics like word count, 
    character count, and sentence count.
    """
    inputs = {
        "text": {
            "type": "string",
            "description": "The text to analyze"
        }
    }
    output_type = "string"
    
    def forward(self, text: str) -> str:
        """Analyze the provided text."""
        try:
            word_count = len(text.split())
            char_count = len(text)
            char_count_no_spaces = len(text.replace(" ", ""))
            sentence_count = len([s for s in text.split('.') if s.strip()])
            
            analysis = {
                "word_count": word_count,
                "character_count": char_count,
                "character_count_no_spaces": char_count_no_spaces,
                "sentence_count": sentence_count,
                "average_word_length": round(char_count_no_spaces / word_count, 2) if word_count > 0 else 0
            }
            
            return f"Text Analysis Results:\n- Words: {analysis['word_count']}\n- Characters: {analysis['character_count']}\n- Characters (no spaces): {analysis['character_count_no_spaces']}\n- Sentences: {analysis['sentence_count']}\n- Average word length: {analysis['average_word_length']} characters"
        except Exception as e:
            return f"Error analyzing text: {str(e)}"

class UrlShortenerTool(Tool):
    """Custom tool to simulate URL shortening."""
    
    name = "url_shortener"
    description = """
    This tool creates a shortened version of a URL.
    """
    inputs = {
        "url": {
            "type": "string",
            "description": "The URL to shorten"
        }
    }
    output_type = "string"
    
    def forward(self, url: str) -> str:
        """Create a shortened URL (mock implementation)."""
        try:
            # Mock URL shortening - in real implementation you'd use a service like bit.ly
            import hashlib
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            shortened_url = f"https://short.ly/{url_hash}"
            return f"Original URL: {url}\nShortened URL: {shortened_url}"
        except Exception as e:
            return f"Error shortening URL: {str(e)}"

def create_agent_with_custom_tools():
    """Create an agent with custom tools."""
    
    # Initialize the Qwen model wrapper
    model = create_qwen_model(
        model_id="ollama_chat/qwen3:latest",
        api_base="http://localhost:11434",
        api_key="dummy_key",
        num_ctx=8192,
        temperature=0.1,
        verbose=True,
    )
    
    # Create custom tool instances
    weather_tool = WeatherTool()
    text_analyzer = TextAnalysisTool()
    url_shortener = UrlShortenerTool()
    
    # Create agent with custom tools
    agent = CodeAgent(
        tools=[weather_tool, text_analyzer, url_shortener],
        model=model,
        add_base_tools=True,  # Also include built-in tools
    )
    
    return agent

def main():
    """Main function to demonstrate custom tools."""
    print("🛠️  Smolagents with Custom Tools Demo")
    print("=" * 50)
    
    try:
        agent = create_agent_with_custom_tools()
        print("✅ Agent with custom tools initialized!")
        
        # List available tools
        print("\n🔧 Available Custom Tools:")
        print("1. weather_checker - Get weather information for a city")
        print("2. text_analyzer - Analyze text statistics")
        print("3. url_shortener - Shorten URLs")
        print("4. Plus all built-in tools (calculator, python_code_interpreter, etc.)")
        
        # Example tasks
        example_tasks = [
            "What's the weather like in Tokyo?",
            "Analyze this text: 'The quick brown fox jumps over the lazy dog. This is a sample sentence for testing.'",
            "Shorten this URL: https://www.example.com/very/long/path/to/some/resource",
            "Calculate the factorial of 5 and then analyze the result as text"
        ]
        
        print("\n🎯 Example tasks:")
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
                
                print(f"\n🤖 Agent is working...")
                result = agent.run(user_input)
                print(f"\n🤖 Agent: {result}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")

if __name__ == "__main__":
    main() 