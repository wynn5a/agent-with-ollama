'use client'

import { motion } from 'framer-motion'
import { User, Bot, Zap, AlertCircle, Copy, Check, Sparkles } from 'lucide-react'
import { useState, useEffect } from 'react'
import { Message } from '@/types/chat'
import { cn, formatTime, formatDuration } from '@/lib/utils'

interface MessageProps {
  message: Message
  isLatest?: boolean
}

export function ChatMessage({ message, isLatest = false }: MessageProps) {
  const [copied, setCopied] = useState(false)
  const [isMounted, setIsMounted] = useState(false)
  const isUser = message.role === 'user'
  const isError = message.status === 'error'
  const isSending = message.status === 'sending'

  useEffect(() => {
    setIsMounted(true)
  }, [])

  const handleCopy = async () => {
    if (message.content) {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.4, 
        ease: [0.16, 1, 0.3, 1],
        delay: isLatest ? 0.1 : 0 
      }}
      className={cn(
        "group relative px-6 py-8 transition-all duration-300",
        isUser 
          ? "ml-12 md:ml-24" 
          : "mr-12 md:mr-24",
        "hover:bg-white/30 dark:hover:bg-black/20"
      )}
    >
      <div className={cn(
        "flex gap-4 items-start",
        isUser && "flex-row-reverse"
      )}>
        {/* Enhanced Avatar */}
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ 
            delay: 0.2, 
            type: "spring", 
            stiffness: 200,
            damping: 15
          }}
          className={cn(
            "relative flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center text-white shadow-xl",
            isUser 
              ? "bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-600 shadow-blue-500/25" 
              : "bg-gradient-to-br from-violet-500 via-purple-600 to-indigo-600 shadow-violet-500/25"
          )}
        >
          {isUser ? (
            <User size={20} />
          ) : (
            <motion.div
              animate={isSending ? { rotate: [0, 360] } : {}}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <Bot size={20} />
            </motion.div>
          )}
          
          {/* Status indicator */}
          {!isUser && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className={cn(
                "absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white",
                isSending ? "bg-yellow-500" : isError ? "bg-red-500" : "bg-emerald-500"
              )}
            >
              {isSending && (
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1, repeat: Infinity }}
                  className="w-full h-full rounded-full bg-yellow-400"
                />
              )}
            </motion.div>
          )}
        </motion.div>

        {/* Message Content */}
        <div className={cn(
          "flex-1 min-w-0 max-w-3xl",
          isUser && "flex flex-col items-end"
        )}>
          {/* Message Bubble */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1, duration: 0.3 }}
            className={cn(
              "relative p-6 rounded-3xl shadow-lg backdrop-blur-sm",
              "border border-white/20 dark:border-gray-700/50",
              isUser
                ? "bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-blue-500/20"
                : "bg-white/80 dark:bg-gray-900/80 text-gray-900 dark:text-white shadow-black/5 dark:shadow-black/20",
              isError && "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800"
            )}
          >
            {/* Header */}
            <div className={cn(
              "flex items-center gap-3 mb-3",
              isUser && "justify-end"
            )}>
              <motion.span 
                className={cn(
                  "text-sm font-semibold",
                  isUser ? "text-blue-100" : "text-gray-700 dark:text-gray-300"
                )}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                {isUser ? 'You' : 'AI Assistant'}
              </motion.span>
              
              {/* Only show timestamp after mount to avoid hydration issues */}
              {isMounted && (
                <motion.span 
                  className={cn(
                    "text-xs",
                    isUser ? "text-blue-200" : "text-gray-500 dark:text-gray-400"
                  )}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  {formatTime(message.timestamp)}
                </motion.span>
              )}
              
              {/* Status indicators */}
              {isSending && (
                <motion.div
                  animate={{ rotate: [0, 360] }}
                  transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                  className="text-yellow-500"
                >
                  <Sparkles size={14} />
                </motion.div>
              )}
              
              {isError && (
                <AlertCircle size={14} className="text-red-500" />
              )}
              
              {message.executionTime && (
                <motion.div 
                  className={cn(
                    "flex items-center gap-1 text-xs px-2 py-1 rounded-full",
                    isUser ? "bg-blue-400/30 text-blue-100" : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
                  )}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <Zap size={10} />
                  {formatDuration(message.executionTime)}
                </motion.div>
              )}
            </div>

            {/* Thinking Process (for assistant messages) */}
            {message.thinking && !isUser && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-2xl border border-yellow-200 dark:border-yellow-800"
              >
                <div className="text-xs font-semibold text-yellow-700 dark:text-yellow-300 mb-2 flex items-center gap-2">
                  <motion.div
                    animate={{ rotate: [0, 360] }}
                    transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                  >
                    🤔
                  </motion.div>
                  Thinking Process
                </div>
                <div className="text-sm text-yellow-800 dark:text-yellow-200 font-mono whitespace-pre-wrap leading-relaxed">
                  {message.thinking}
                </div>
              </motion.div>
            )}

            {/* Message Content */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.4 }}
              className="relative"
            >
              {isSending ? (
                <div className="flex items-center gap-3">
                  <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                  <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Thinking...
                  </span>
                </div>
              ) : (
                <div className={cn(
                  "prose prose-slate dark:prose-invert max-w-none",
                  "prose-pre:bg-gray-100 dark:prose-pre:bg-gray-800",
                  "prose-code:bg-gray-100 dark:prose-code:bg-gray-800",
                  "prose-code:px-2 prose-code:py-1 prose-code:rounded-md",
                  "leading-relaxed",
                  isUser && "prose-invert",
                  isError && "text-red-600 dark:text-red-400"
                )}>
                  <div className="whitespace-pre-wrap break-words">
                    {message.content}
                  </div>
                </div>
              )}
            </motion.div>

            {/* Copy button */}
            {!isSending && !isUser && (
              <motion.button
                onClick={handleCopy}
                className="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                {copied ? (
                  <Check size={16} className="text-green-500" />
                ) : (
                  <Copy size={16} />
                )}
              </motion.button>
            )}

            {/* Message tail */}
            <div className={cn(
              "absolute top-6 w-4 h-4 rotate-45",
              isUser
                ? "right-[-8px] bg-gradient-to-br from-blue-500 to-indigo-600"
                : "left-[-8px] bg-white/80 dark:bg-gray-900/80 border-l border-t border-white/20 dark:border-gray-700/50"
            )} />
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
} 