#!/bin/bash

# Smolagents + Ollama Setup Script
# This script helps set up the project environment

set -e  # Exit on any error

echo "🚀 Smolagents + Ollama Setup Script"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo "📥 Installing Ollama..."
    
    # Detect OS and install Ollama
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo "❌ Homebrew not found. Please install Ollama manually from https://ollama.ai"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported OS. Please install Ollama manually from https://ollama.ai"
        exit 1
    fi
else
    echo "✅ Ollama found: $(ollama --version)"
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp config.env.example .env
    echo "✅ Created .env file. You can customize it if needed."
fi

# Start Ollama service (in background)
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait a moment for Ollama to start
sleep 3

# Pull the Qwen3 model
echo "📥 Pulling Qwen3 model (this may take a while)..."
ollama pull qwen3:latest

# Run tests
echo "🧪 Running setup tests..."
python test_setup.py

# Stop Ollama if we started it
if [ ! -z "$OLLAMA_PID" ]; then
    echo "🛑 Stopping Ollama service..."
    kill $OLLAMA_PID 2>/dev/null || true
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the agent: python main.py"
echo ""
echo "💡 Or run the test script to verify everything works: python test_setup.py" 