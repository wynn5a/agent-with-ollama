# AI Agent Chat UI

A beautiful, modern chat interface for your local AI agent powered by Qwen3 and Ollama.

![AI Agent Chat UI](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38B2AC?style=for-the-badge&logo=tailwind-css)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-11-FF0055?style=for-the-badge&logo=framer)

## ✨ Features

- **🎨 Beautiful Modern UI**: Glass effects, smooth animations, and responsive design
- **⚡ Real-time Chat**: Instant messaging with typing indicators and status updates
- **🤖 AI Agent Integration**: Direct connection to your local Qwen3 agent via Ollama
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **🌙 Dark Mode Support**: Automatic dark/light mode based on system preferences
- **⏱️ Performance Metrics**: Execution time tracking and connection status
- **🔄 Real-time Updates**: Live status indicators and processing feedback
- **💫 Smooth Animations**: Framer Motion powered transitions and micro-interactions

## 🚀 Quick Start

### Prerequisites

1. **Node.js 18+** - [Download here](https://nodejs.org/)
2. **Ollama** - [Install Ollama](https://ollama.ai/)
3. **Qwen3 Model** - Run `ollama pull qwen3:latest`
4. **Python Backend** - The FastAPI server from the parent directory

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Using the Startup Script

For the complete experience, use the startup script from the parent directory:

```bash
cd ..
python start_chat_ui.py
```

This will start both the Python backend and Next.js frontend automatically.

## 🏗️ Architecture

### Frontend Stack
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons

### Backend Integration
- **FastAPI** - Python REST API server
- **Ollama** - Local LLM inference
- **Qwen3** - Advanced language model
- **smolagents** - Agent framework

### Project Structure
```
agent-ui/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── api/chat/        # API routes
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/
│   │   └── chat/            # Chat components
│   │       ├── chat-header.tsx
│   │       ├── chat-input.tsx
│   │       ├── chat-interface.tsx
│   │       └── message.tsx
│   ├── lib/
│   │   └── utils.ts         # Utility functions
│   └── types/
│       └── chat.ts          # TypeScript types
├── public/                  # Static assets
├── package.json
└── README.md
```

## 🎨 UI Components

### ChatInterface
The main chat container that manages state and coordinates all components.

### ChatHeader
Displays agent status, connection info, and settings with animated indicators.

### ChatMessage
Individual message bubbles with user/assistant avatars, timestamps, and status indicators.

### ChatInput
Advanced input component with auto-resize, keyboard shortcuts, and send/stop controls.

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file:

```env
# Python backend URL (default: http://localhost:8000)
PYTHON_BACKEND_URL=http://localhost:8000

# Next.js configuration
NEXT_PUBLIC_APP_NAME="AI Agent Chat"
NEXT_PUBLIC_APP_VERSION="1.0.0"
```

### Customization

#### Colors and Themes
Edit `src/app/globals.css` to customize the color palette:

```css
:root {
  --primary: 239 68 68; /* red-500 */
  --accent: 59 130 246;  /* blue-500 */
  /* ... more colors */
}
```

#### Animation Settings
Modify animation durations in component files or `globals.css`:

```css
.message-enter {
  animation: messageEnter 0.3s ease-out;
}
```

## 📡 API Integration

### Chat Endpoint
```typescript
POST /api/chat
{
  "message": "Hello, AI agent!"
}

Response:
{
  "response": "Hello! How can I help you today?",
  "executionTime": 1.23,
  "thinking": "...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Status Endpoint
```typescript
GET /api/status
{
  "status": "connected",
  "model": "qwen3:latest",
  "endpoint": "http://localhost:11434",
  "isConnected": true,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🎯 Features in Detail

### Real-time Status Indicators
- **Connection Status**: Green/red indicators for Ollama connectivity
- **Processing State**: Animated indicators when AI is thinking
- **Message Status**: Sending, sent, and error states

### Advanced Input Features
- **Auto-resize**: Text area grows with content
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line
- **Voice Input**: Placeholder for future voice integration
- **File Attachments**: Placeholder for future file uploads

### Performance Monitoring
- **Execution Time**: Track how long each response takes
- **Connection Health**: Monitor backend connectivity
- **Message Count**: Track conversation length

### Responsive Design
- **Mobile First**: Optimized for mobile devices
- **Tablet Support**: Perfect layout for tablets
- **Desktop Experience**: Full-featured desktop interface

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Docker (Optional)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔍 Troubleshooting

### Common Issues

1. **"Cannot connect to AI agent"**
   - Ensure Ollama is running: `ollama serve`
   - Check if Qwen3 is installed: `ollama list`
   - Verify Python backend is running on port 8000

2. **"Module not found" errors**
   - Run `npm install` to install dependencies
   - Clear Next.js cache: `rm -rf .next`

3. **Styling issues**
   - Ensure Tailwind CSS is properly configured
   - Check for conflicting CSS imports

4. **Animation performance**
   - Reduce animation complexity in `globals.css`
   - Disable animations for slower devices

### Debug Mode

Enable verbose logging by setting:
```env
NODE_ENV=development
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is part of the AI Agent with Ollama suite. See the main project for license information.

## 🙏 Acknowledgments

- **Ollama Team** - For the amazing local LLM platform
- **Qwen Team** - For the powerful language model
- **Next.js Team** - For the excellent React framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Framer Motion** - For beautiful animations

---

**Happy Chatting! 🤖💬**
