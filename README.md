# Smolagents with Local Ollama Integration

A powerful AI agent framework using [smolagents](https://github.com/huggingface/smolagents) with local Ollama models. This project demonstrates how to create intelligent agents that can reason, use tools, and execute code using your local Qwen3 model.

## 🚀 Features

- **Local AI Model**: Uses your local Ollama `qwen3:latest` model
- **Built-in Tools**: Calculator, Python code interpreter, and more
- **Custom Tools**: Extensible framework for adding custom functionality
- **Batch Processing**: Process multiple tasks efficiently
- **Interactive Mode**: Real-time conversation with the agent
- **Professional Code**: Clean, maintainable, and well-documented

## 📋 Prerequisites

### 1. Ollama Installation

First, install Ollama on your system:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Pull the Qwen3 Model

```bash
ollama pull qwen3:latest
```

### 3. Start Ollama Server

```bash
ollama serve
```

Verify it's running by visiting `http://localhost:11434` in your browser.

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd agent-with-ollama
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional):
```bash
cp config.env.example .env
# Edit .env file if you need custom settings
```

## 🎯 Usage

### Basic Agent

Run the main agent script for interactive mode:

```bash
python main.py
```

This will start an interactive session where you can:
- Ask mathematical questions
- Request code generation and execution
- Perform calculations
- Get help with various tasks

**Example interactions**:
```
🧑 You: Calculate the 10th Fibonacci number
🤖 Agent: I'll calculate the 10th Fibonacci number for you...

🧑 You: Write a Python function to reverse a string and test it
🤖 Agent: I'll create a function to reverse a string and test it...
```

### Custom Tools Example

Run the custom tools demo to see extended functionality:

```bash
python examples/custom_tools.py
```

This includes additional tools like:
- **Weather Checker**: Get weather information for cities
- **Text Analyzer**: Analyze text statistics
- **URL Shortener**: Create shortened URLs

### Batch Processing

Process multiple tasks efficiently:

```bash
python examples/batch_processing.py
```

Features:
- Process predefined task lists
- Generate execution reports
- Save results to JSON files
- Performance metrics

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `config.env.example`:

```env
# Ollama Configuration
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_MODEL=qwen3:latest
OLLAMA_CONTEXT_SIZE=8192
OLLAMA_TEMPERATURE=0.1
MAX_ITERATIONS=10
```

### Model Configuration

The agent is configured with optimal settings for the Qwen3 model:

- **Context Size**: 8192 tokens (important for agent reasoning)
- **Temperature**: 0.1 (low for consistent responses)
- **Max Iterations**: 10 (prevents infinite loops)

## 🛠️ Creating Custom Tools

You can extend the agent with custom tools. Here's a simple example:

```python
from smolagents import Tool

class MyCustomTool(Tool):
    name = "my_tool"
    description = "Description of what this tool does"
    inputs = {
        "input_param": {
            "type": "string",
            "description": "Description of the input parameter"
        }
    }
    output_type = "string"
    
    def forward(self, input_param: str) -> str:
        # Your tool logic here
        return f"Processed: {input_param}"

# Add to agent
tool = MyCustomTool()
agent = CodeAgent(tools=[tool], model=model, add_base_tools=True)
```

## 📊 Built-in Tools

The agent comes with several built-in tools:

- **Calculator**: Perform mathematical calculations
- **Python Code Interpreter**: Execute Python code safely
- **Web Search**: Search for information online (if configured)
- **File Operations**: Read and write files

## 🔍 Troubleshooting

### Common Issues

1. **"Connection refused" error**:
   ```bash
   # Make sure Ollama is running
   ollama serve
   ```

2. **Model not found**:
   ```bash
   # Pull the model
   ollama pull qwen3:latest
   
   # Verify it's available
   ollama list
   ```

3. **Out of memory errors**:
   - Reduce `OLLAMA_CONTEXT_SIZE` in your `.env` file
   - Use a smaller model if available

4. **Slow responses**:
   - Ensure you have sufficient RAM (8GB+ recommended)
   - Close other applications to free up resources

### Performance Tips

- **RAM**: 8GB+ recommended for optimal performance
- **Context Size**: Start with 4096 if 8192 is too large
- **Temperature**: Keep low (0.1-0.3) for consistent agent behavior
- **Iterations**: Limit to 5-10 to prevent long execution times

## 🏗️ Project Structure

```
agent-with-ollama/
├── main.py                    # Main agent script
├── requirements.txt           # Python dependencies
├── config.env.example        # Environment configuration template
├── examples/
│   ├── custom_tools.py       # Custom tools demonstration
│   └── batch_processing.py   # Batch processing example
└── README.md                 # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face Smolagents](https://github.com/huggingface/smolagents) - The core agent framework
- [Ollama](https://ollama.ai/) - Local LLM serving
- [Qwen](https://github.com/QwenLM/Qwen) - The language model

## 📚 Additional Resources

- [Smolagents Documentation](https://huggingface.co/docs/smolagents)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/README.md)
- [Qwen Model Documentation](https://huggingface.co/Qwen)

---

**Happy coding with your local AI agent! 🤖✨**