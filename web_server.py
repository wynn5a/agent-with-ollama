#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI Web Server for AI Agent Chat UI

This server provides a REST API interface for the Next.js chat UI
to communicate with the local AI agent.
"""

import os
import sys
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(__file__))

# Import our existing agent components
try:
    from utils.qwen_model_wrapper import create_qwen_model
    from smolagents import CodeAgent
except ImportError as e:
    print(f"❌ Error importing agent components: {e}")
    print("Make sure you're running this from the agent-with-ollama directory")
    sys.exit(1)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    timestamp: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    executionTime: float
    thinking: Optional[str] = None
    timestamp: str

class StatusResponse(BaseModel):
    status: str
    model: str
    endpoint: str
    isConnected: bool
    timestamp: str

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent Chat API",
    description="REST API for AI Agent Chat Interface",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None
agent_config = {
    "model_id": "ollama_chat/qwen3:latest",
    "api_base": "http://localhost:11434",
    "api_key": "dummy_key",
    "num_ctx": 8192,
    "temperature": 0.1,
    "verbose": False,  # Disable verbose for web interface
}

def initialize_agent():
    """Initialize the AI agent."""
    global agent
    try:
        print("🔧 Initializing AI agent...")
        
        # Create the Qwen model wrapper
        model = create_qwen_model(**agent_config)
        
        # Create the agent
        agent = CodeAgent(
            tools=[],
            model=model,
            add_base_tools=True,
        )
        
        print("✅ AI agent initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return False

def check_ollama_connection():
    """Check if Ollama is running and accessible."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the agent when the server starts."""
    print("🚀 Starting AI Agent Chat API Server...")
    
    # Check Ollama connection
    if not check_ollama_connection():
        print("⚠️  Warning: Cannot connect to Ollama at http://localhost:11434")
        print("   Make sure Ollama is running: ollama serve")
    
    # Initialize agent
    if not initialize_agent():
        print("⚠️  Warning: Agent initialization failed")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Agent Chat API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "chat": "POST /chat",
            "status": "GET /status",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    ollama_connected = check_ollama_connection()
    agent_ready = agent is not None
    
    return {
        "status": "healthy" if (ollama_connected and agent_ready) else "degraded",
        "ollama_connected": ollama_connected,
        "agent_ready": agent_ready,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get agent status."""
    ollama_connected = check_ollama_connection()
    
    return StatusResponse(
        status="connected" if ollama_connected else "disconnected",
        model=agent_config["model_id"],
        endpoint=agent_config["api_base"],
        isConnected=ollama_connected and agent is not None,
        timestamp=datetime.now().isoformat()
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Send a message to the AI agent and get a response."""
    if agent is None:
        raise HTTPException(
            status_code=503, 
            detail="AI agent is not initialized. Please check server logs."
        )
    
    if not check_ollama_connection():
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Please make sure Ollama is running."
        )
    
    try:
        print(f"💬 Received message: {request.message[:100]}...")
        
        start_time = time.time()
        
        # Run the agent in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            agent.run, 
            request.message
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"✅ Response generated in {execution_time:.2f}s")
        
        # Ensure response is always a string
        response_str = str(response) if response is not None else "No response generated"
        
        return ChatResponse(
            response=response_str,
            executionTime=execution_time,
            thinking=None,  # We could extract thinking tags here if needed
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"❌ Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.post("/chat/stop")
async def stop_chat():
    """Stop the current chat processing (placeholder for future implementation)."""
    return {"message": "Stop request received", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🤖 AI Agent Chat API Server")
    print("=" * 50)
    print("This server provides a REST API for the Next.js chat interface")
    print("to communicate with your local AI agent.")
    print()
    print("Prerequisites:")
    print("1. Ollama should be running: ollama serve")
    print("2. Qwen3 model should be available: ollama pull qwen3:latest")
    print()
    print("Starting server...")
    
    # Run the server
    uvicorn.run(
        "web_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 