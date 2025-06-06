#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup script for AI Agent Chat UI

This script starts both the Python backend and Next.js frontend.
"""

import os
import sys
import time
import subprocess
import signal
import threading
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed."""
    print("🔍 Checking requirements...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import smolagents
        print("✅ Python dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Check if Node.js is available
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js is available: {result.stdout.strip()}")
        else:
            print("❌ Node.js is not available")
            return False
    except FileNotFoundError:
        print("❌ Node.js is not installed")
        print("Please install Node.js from https://nodejs.org/")
        return False
    
    # Check if agent-ui directory exists
    ui_dir = Path("agent-ui")
    if not ui_dir.exists():
        print("❌ agent-ui directory not found")
        return False
    
    # Check if package.json exists
    package_json = ui_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found in agent-ui directory")
        return False
    
    print("✅ All requirements check passed")
    return True

def check_ollama():
    """Check if Ollama is running."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("⚠️  Ollama is not responding properly")
            return False
    except Exception:
        print("⚠️  Ollama is not running")
        print("Please start Ollama: ollama serve")
        return False

def install_ui_dependencies():
    """Install Next.js dependencies if needed."""
    ui_dir = Path("agent-ui")
    node_modules = ui_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing Next.js dependencies...")
        try:
            subprocess.run(
                ["npm", "install"], 
                cwd=ui_dir, 
                check=True,
                capture_output=True
            )
            print("✅ Next.js dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    else:
        print("✅ Next.js dependencies already installed")
        return True

def start_backend():
    """Start the Python backend server."""
    print("🚀 Starting Python backend server...")
    try:
        # Start the backend server
        process = subprocess.Popen(
            [sys.executable, "web_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print backend output
        def print_backend_output():
            for line in process.stdout:
                print(f"[Backend] {line.rstrip()}")
        
        threading.Thread(target=print_backend_output, daemon=True).start()
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend."""
    print("🎨 Starting Next.js frontend...")
    ui_dir = Path("agent-ui")
    
    try:
        # Start the frontend server
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=ui_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print frontend output
        def print_frontend_output():
            for line in process.stdout:
                print(f"[Frontend] {line.rstrip()}")
        
        threading.Thread(target=print_frontend_output, daemon=True).start()
        return process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main startup function."""
    print("🤖 AI Agent Chat UI Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check Ollama (warning only)
    check_ollama()
    
    # Install UI dependencies
    if not install_ui_dependencies():
        sys.exit(1)
    
    print("\n🚀 Starting servers...")
    print("Backend will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers")
    print("-" * 50)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        sys.exit(1)
    
    # Handle shutdown
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for processes
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()

if __name__ == "__main__":
    main() 