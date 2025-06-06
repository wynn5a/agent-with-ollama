'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChatHeader } from './chat-header'
import { ChatMessage } from './message'
import { ChatInput } from './chat-input'
import { Message, AgentStatus } from '@/types/chat'
import { generateId } from '@/lib/utils'
import { Sparkles, Zap, Code, Calculator, Brain, MessageSquare } from 'lucide-react'

const SUGGESTED_PROMPTS = [
  {
    icon: Calculator,
    title: "Calculate the factorial of 10",
    description: "Mathematical computation"
  },
  {
    icon: Code,
    title: "Write a Python function to reverse a string",
    description: "Code generation"
  },
  {
    icon: Brain,
    title: "Explain quantum computing in simple terms",
    description: "Educational content"
  },
  {
    icon: Zap,
    title: "Generate a secure random password",
    description: "Utility function"
  }
]

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [isMounted, setIsMounted] = useState(false)
  const [particlePositions, setParticlePositions] = useState<Array<{top: string, left: string}>>([])
  const [status, setStatus] = useState<AgentStatus>({
    isConnected: true,
    isProcessing: false,
    model: 'qwen3:latest',
    endpoint: 'http://localhost:11434',
  })
  
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const abortControllerRef = useRef<AbortController | null>(null)

  // Initialize client-side only values
  useEffect(() => {
    setIsMounted(true)
    // Generate particle positions only on client side
    const positions = [...Array(6)].map(() => ({
      top: `${Math.random() * 100}%`,
      left: `${Math.random() * 100}%`,
    }))
    setParticlePositions(positions)
  }, [])

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Check connection status
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch('/api/health', { method: 'GET' })
        setStatus(prev => ({ ...prev, isConnected: response.ok }))
      } catch {
        setStatus(prev => ({ ...prev, isConnected: false }))
      }
    }

    checkConnection()
    const interval = setInterval(checkConnection, 30000) // Check every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const sendToAgent = async (message: string): Promise<string> => {
    abortControllerRef.current = new AbortController()
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
        signal: abortControllerRef.current.signal,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.response
    } catch (error) {
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request was cancelled')
        }
        throw error
      }
      throw new Error('Unknown error occurred')
    }
  }

  const handleSendMessage = async (content: string) => {
    if (isProcessing || !isMounted) return

    // Add user message
    const userMessage: Message = {
      id: generateId(),
      content,
      role: 'user',
      timestamp: new Date(),
      status: 'sent',
    }

    setMessages(prev => [...prev, userMessage])
    setIsProcessing(true)
    setStatus(prev => ({ ...prev, isProcessing: true }))

    // Add assistant message with loading state
    const assistantMessageId = generateId()
    const assistantMessage: Message = {
      id: assistantMessageId,
      content: '',
      role: 'assistant',
      timestamp: new Date(),
      status: 'sending',
    }

    setMessages(prev => [...prev, assistantMessage])

    try {
      const startTime = Date.now()
      const response = await sendToAgent(content)
      const endTime = Date.now()
      const executionTime = (endTime - startTime) / 1000

      // Update assistant message with response
      setMessages(prev => prev.map(msg => 
        msg.id === assistantMessageId 
          ? { 
              ...msg, 
              content: response, 
              status: 'sent',
              executionTime 
            }
          : msg
      ))
    } catch (error) {
      // Update assistant message with error
      setMessages(prev => prev.map(msg => 
        msg.id === assistantMessageId 
          ? { 
              ...msg, 
              content: error instanceof Error ? error.message : 'An error occurred', 
              status: 'error' 
            }
          : msg
      ))
    } finally {
      setIsProcessing(false)
      setStatus(prev => ({ ...prev, isProcessing: false }))
      abortControllerRef.current = null
    }
  }

  const handleStopProcessing = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
  }

  const handleSettingsClick = () => {
    console.log('Settings clicked')
  }

  // Don't render content with random values until mounted
  if (!isMounted) {
    return (
      <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <ChatHeader 
          status={status}
          onSettingsClick={handleSettingsClick}
          messageCount={0}
        />
        <div className="flex-1 flex items-center justify-center">
          <div className="spinner" />
        </div>
        <ChatInput
          onSendMessage={() => {}}
          isProcessing={false}
          onStopProcessing={() => {}}
          disabled={true}
        />
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <ChatHeader 
        status={status}
        onSettingsClick={handleSettingsClick}
        messageCount={messages.length}
      />

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto">
          {messages.length === 0 ? (
            <motion.div 
              className="flex flex-col items-center justify-center h-full min-h-[500px] text-center px-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              {/* Hero Section */}
              <motion.div
                className="relative mb-8"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.5 }}
              >
                <div className="w-24 h-24 bg-gradient-to-br from-violet-500 via-purple-600 to-indigo-600 rounded-3xl flex items-center justify-center text-white shadow-2xl shadow-violet-500/25 mb-6">
                  <motion.div
                    animate={{ rotate: [0, 360] }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  >
                    <Sparkles size={40} />
                  </motion.div>
                </div>
                
                {/* Floating particles */}
                {particlePositions.map((position, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-2 h-2 bg-violet-400 rounded-full"
                    style={{
                      top: position.top,
                      left: position.left,
                    }}
                    animate={{
                      y: [0, -20, 0],
                      opacity: [0.3, 1, 0.3],
                    }}
                    transition={{
                      duration: 3 + Math.random() * 2,
                      repeat: Infinity,
                      delay: Math.random() * 2,
                    }}
                  />
                ))}
              </motion.div>
              
              <motion.h1 
                className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-900 via-violet-800 to-indigo-900 dark:from-white dark:via-violet-200 dark:to-indigo-200 bg-clip-text text-transparent mb-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3, duration: 0.5 }}
              >
                Welcome to AI Agent
              </motion.h1>
              
              <motion.p 
                className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mb-8 leading-relaxed"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.5 }}
              >
                Your intelligent assistant powered by <span className="font-semibold text-violet-600 dark:text-violet-400">Qwen3</span> and <span className="font-semibold text-indigo-600 dark:text-indigo-400">Ollama</span>. 
                Ask me anything - from complex calculations to creative writing, code generation to problem solving!
              </motion.p>
              
              {/* Suggested Prompts */}
              <motion.div 
                className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-4xl"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5, duration: 0.5 }}
              >
                {SUGGESTED_PROMPTS.map((prompt, index) => (
                  <motion.button
                    key={prompt.title}
                    onClick={() => handleSendMessage(prompt.title)}
                    className="group p-6 text-left bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm border border-white/20 dark:border-gray-700/50 rounded-2xl hover:bg-white/90 dark:hover:bg-gray-800/90 transition-all duration-300 shadow-lg hover:shadow-xl card-hover"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 + index * 0.1, duration: 0.4 }}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="flex items-start gap-4">
                      <div className="p-3 bg-gradient-to-br from-violet-500 to-indigo-600 rounded-xl text-white shadow-lg group-hover:shadow-violet-500/25 transition-shadow">
                        <prompt.icon size={24} />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-1 group-hover:text-violet-600 dark:group-hover:text-violet-400 transition-colors">
                          {prompt.title}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {prompt.description}
                        </p>
                      </div>
                    </div>
                  </motion.button>
                ))}
              </motion.div>

              {/* Features */}
              <motion.div 
                className="mt-12 flex flex-wrap justify-center gap-6 text-sm text-gray-500 dark:text-gray-400"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8, duration: 0.5 }}
              >
                <div className="flex items-center gap-2">
                  <MessageSquare size={16} />
                  <span>Natural conversation</span>
                </div>
                <div className="flex items-center gap-2">
                  <Code size={16} />
                  <span>Code generation</span>
                </div>
                <div className="flex items-center gap-2">
                  <Brain size={16} />
                  <span>Problem solving</span>
                </div>
                <div className="flex items-center gap-2">
                  <Zap size={16} />
                  <span>Fast responses</span>
                </div>
              </motion.div>
            </motion.div>
          ) : (
            <div className="py-8">
              <AnimatePresence>
                {messages.map((message, index) => (
                  <ChatMessage
                    key={message.id}
                    message={message}
                    isLatest={index === messages.length - 1}
                  />
                ))}
              </AnimatePresence>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput
        onSendMessage={handleSendMessage}
        isProcessing={isProcessing}
        onStopProcessing={handleStopProcessing}
        disabled={!status.isConnected}
      />
    </div>
  )
} 