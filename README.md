# AI Agent with Ollama

A powerful AI agent system powered by Qwen3 and Ollama, featuring both command-line tools and a beautiful modern web interface.

## ✨ Features

### 🤖 Core Agent Capabilities
- **Local AI Processing**: Powered by Qwen3 via Ollama - no cloud dependencies
- **Code Generation & Execution**: Write, run, and debug code in multiple languages
- **Tool Integration**: Built-in tools for calculations, web search, and more
- **Batch Processing**: Process multiple tasks efficiently with retry logic
- **Thinking Tags Support**: Advanced reasoning with visible thought processes

### 🎨 Beautiful Web Interface
- **Modern Chat UI**: Beautiful, responsive interface built with Next.js 15
- **Real-time Communication**: Instant messaging with typing indicators
- **Smooth Animations**: Framer Motion powered transitions and micro-interactions
- **Dark Mode Support**: Automatic theme switching based on system preferences
- **Performance Monitoring**: Execution time tracking and connection status
- **Mobile Responsive**: Perfect experience across all devices

## 🚀 Quick Start

### Prerequisites

1. **Ollama** - [Install Ollama](https://ollama.ai/)
2. **Qwen3 Model** - Run `ollama pull qwen3:latest`
3. **Python 3.8+** - [Download Python](https://python.org/)
4. **Node.js 18+** (for web UI) - [Download Node.js](https://nodejs.org/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd agent-with-ollama
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama (if not already running):**
   ```bash
   ollama serve
   ```

### Usage Options

#### 🎨 Web Interface (Recommended)
Launch the beautiful chat interface:
```bash
python start_chat_ui.py
```

This will start both the Python backend (port 8000) and Next.js frontend (port 3000).
Open [http://localhost:3000](http://localhost:3000) in your browser.

#### 💻 Command Line Interface
For direct command-line usage:
```bash
python main.py
```

#### 📦 Batch Processing
Process multiple tasks from a file:
```bash
python examples/batch_processing.py
```

## 🏗️ Architecture

### Core Components
- **QwenModelWrapper**: Custom wrapper handling Qwen3's thinking tags
- **CodeAgent**: Main agent with tool integration and code execution
- **Web Server**: FastAPI backend for the chat interface
- **Chat UI**: Modern Next.js frontend with TypeScript and Tailwind CSS

### Project Structure
```
agent-with-ollama/
├── agent-ui/                    # Next.js chat interface
│   ├── src/
│   │   ├── app/                # App router and API routes
│   │   │   └── types/             # TypeScript definitions
│   │   └── package.json
│   ├── examples/
│   │   ├── batch_processing.py    # Batch task processing
│   │   └── tasks.txt             # Sample tasks
│   ├── utils/
│   │   └── qwen_model_wrapper.py # Qwen3 integration
│   ├── main.py                   # CLI interface
│   ├── web_server.py            # FastAPI backend
│   └── start_chat_ui.py         # Startup script
└── requirements.txt
```

## 🎯 Features in Detail

### Web Interface Features
- **Real-time Chat**: Instant messaging with the AI agent
- **Status Indicators**: Live connection and processing status
- **Execution Metrics**: Track response times and performance
- **Message History**: Persistent conversation history
- **Error Handling**: Graceful error display and retry mechanisms
- **Responsive Design**: Works on desktop, tablet, and mobile

### Agent Capabilities
- **Code Generation**: Write functions, scripts, and complete programs
- **Mathematical Calculations**: Solve complex equations and problems
- **Text Processing**: Analysis, summarization, and transformation
- **Problem Solving**: Step-by-step reasoning and solution development
- **Tool Usage**: Integrated calculator, web search, and more

### Advanced Features
- **Thinking Process Visibility**: See how the AI reasons through problems
- **Retry Logic**: Automatic retry with exponential backoff
- **Timeout Handling**: Configurable timeouts for long-running tasks
- **Error Recovery**: Graceful handling of failures and edge cases

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
# Ollama Configuration
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_MODEL=qwen3:latest

# Agent Settings
AGENT_TEMPERATURE=0.1
AGENT_MAX_TOKENS=8192
AGENT_VERBOSE=false

# Web UI Settings
PYTHON_BACKEND_URL=http://localhost:8000
```

### Model Configuration
The agent uses Qwen3 by default, but you can configure other models:
```python
agent_config = {
    "model_id": "ollama_chat/qwen3:latest",
    "api_base": "http://localhost:11434",
    "temperature": 0.1,
    "num_ctx": 8192,
}
```

## 📚 Examples

### Basic Chat
```python
from utils.qwen_model_wrapper import create_qwen_model
from smolagents import CodeAgent

model = create_qwen_model()
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

response = agent.run("Calculate the factorial of 10")
print(response)
```

### Batch Processing
```python
tasks = [
    "Write a Python function to reverse a string",
    "Calculate the area of a circle with radius 5",
    "Explain quantum computing in simple terms"
]

# Process with the batch script
python examples/batch_processing.py
```

### Web API Usage
```bash
# Start the web server
python web_server.py

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI agent!"}'
```

## 🔍 Troubleshooting

### Common Issues

1. **"Cannot connect to Ollama"**
   ```bash
   # Start Ollama
   ollama serve
   
   # Verify it's running
   curl http://localhost:11434/api/tags
   ```

2. **"Model not found"**
   ```bash
   # Pull the Qwen3 model
   ollama pull qwen3:latest
   
   # List available models
   ollama list
   ```

3. **"Thinking tags not handled"**
   - Ensure you're using `QwenModelWrapper` instead of raw `LiteLLMModel`
   - Check that the wrapper is properly configured

4. **Web UI connection issues**
   - Verify Python backend is running on port 8000
   - Check CORS settings in `web_server.py`
   - Ensure Next.js is running on port 3000

### Debug Mode
Enable verbose logging:
```bash
# For CLI
python main.py --verbose

# For web server
AGENT_VERBOSE=true python web_server.py
```

## 🚀 Deployment

### Development
```bash
# Start everything
python start_chat_ui.py

# Or start components separately
python web_server.py  # Backend on port 8000
cd agent-ui && npm run dev  # Frontend on port 3000
```

### Production
```bash
# Build the frontend
cd agent-ui
npm run build

# Start production servers
python web_server.py
cd agent-ui && npm start
```

### Docker (Optional)
```dockerfile
# Multi-stage build for the complete stack
FROM python:3.11-slim as backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM node:18-alpine as frontend
WORKDIR /app/agent-ui
COPY agent-ui/package*.json ./
RUN npm ci
COPY agent-ui/ .
RUN npm run build

# Production image
FROM python:3.11-slim
WORKDIR /app
COPY --from=backend /app .
COPY --from=frontend /app/agent-ui/.next ./agent-ui/.next
EXPOSE 8000 3000
CMD ["python", "start_chat_ui.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Add tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team** - For the amazing local LLM platform
- **Qwen Team** - For the powerful Qwen3 language model
- **smolagents** - For the excellent agent framework
- **Next.js Team** - For the outstanding React framework
- **Tailwind CSS** - For the utility-first CSS framework

---

**Ready to chat with your AI agent? 🤖💬**

Get started with: `python start_chat_ui.py`