'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Square, Mic, Paperclip, Sparkles } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  isProcessing: boolean
  onStopProcessing?: () => void
  placeholder?: string
  disabled?: boolean
}

export function ChatInput({ 
  onSendMessage, 
  isProcessing, 
  onStopProcessing,
  placeholder = "Ask your AI agent anything...",
  disabled = false
}: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !isProcessing && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
      adjustTextareaHeight()
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [message])

  const handleStop = () => {
    if (onStopProcessing) {
      onStopProcessing()
    }
  }

  return (
    <motion.div 
      className="glass-morphism border-t border-white/10"
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      <div className="max-w-5xl mx-auto p-6">
        <motion.form
          onSubmit={handleSubmit}
          className={cn(
            "relative flex items-end gap-4 p-4 rounded-3xl transition-all duration-300",
            "bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-2",
            "shadow-xl shadow-black/5 dark:shadow-black/20",
            isFocused 
              ? "border-violet-500/50 shadow-violet-500/20 dark:shadow-violet-500/10" 
              : "border-gray-200/50 dark:border-gray-700/50",
            disabled && "opacity-50 cursor-not-allowed"
          )}
          whileFocus={{ scale: 1.01 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        >
          {/* Attachment button */}
          <motion.button
            type="button"
            className="flex-shrink-0 p-3 text-gray-500 hover:text-violet-600 dark:text-gray-400 dark:hover:text-violet-400 transition-colors rounded-2xl hover:bg-gray-100/50 dark:hover:bg-gray-800/50 disabled:opacity-50"
            disabled={disabled}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Paperclip size={20} />
          </motion.button>

          {/* Text input */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              placeholder={placeholder}
              disabled={disabled}
              className={cn(
                "w-full resize-none border-0 bg-transparent text-gray-900 dark:text-white",
                "placeholder:text-gray-500 dark:placeholder:text-gray-400",
                "focus:outline-none focus:ring-0",
                "min-h-[28px] max-h-[120px] leading-7 text-base font-medium"
              )}
              rows={1}
            />
            
            {/* Character count indicator */}
            <AnimatePresence>
              {message.length > 100 && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="absolute -top-8 right-0 text-xs text-gray-500 dark:text-gray-400"
                >
                  {message.length}/1000
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Voice input button */}
          <motion.button
            type="button"
            className="flex-shrink-0 p-3 text-gray-500 hover:text-violet-600 dark:text-gray-400 dark:hover:text-violet-400 transition-colors rounded-2xl hover:bg-gray-100/50 dark:hover:bg-gray-800/50 disabled:opacity-50"
            disabled={disabled}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Mic size={20} />
          </motion.button>

          {/* Send/Stop button */}
          <motion.button
            type={isProcessing ? "button" : "submit"}
            onClick={isProcessing ? handleStop : undefined}
            disabled={disabled || (!message.trim() && !isProcessing)}
            className={cn(
              "flex-shrink-0 p-3 rounded-2xl transition-all duration-200 font-medium",
              "disabled:opacity-50 disabled:cursor-not-allowed",
              "shadow-lg",
              isProcessing
                ? "bg-red-500 hover:bg-red-600 text-white shadow-red-500/25"
                : message.trim()
                ? "bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-white shadow-violet-500/25"
                : "bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
            )}
            whileHover={message.trim() || isProcessing ? { scale: 1.05 } : {}}
            whileTap={message.trim() || isProcessing ? { scale: 0.95 } : {}}
          >
            <AnimatePresence mode="wait">
              {isProcessing ? (
                <motion.div
                  key="stop"
                  initial={{ rotate: 180, opacity: 0 }}
                  animate={{ rotate: 0, opacity: 1 }}
                  exit={{ rotate: -180, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <Square size={20} />
                </motion.div>
              ) : (
                <motion.div
                  key="send"
                  initial={{ rotate: -180, opacity: 0 }}
                  animate={{ rotate: 0, opacity: 1 }}
                  exit={{ rotate: 180, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <Send size={20} />
                </motion.div>
              )}
            </AnimatePresence>
          </motion.button>
        </motion.form>

        {/* Enhanced helper text */}
        <motion.div 
          className="mt-4 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <AnimatePresence mode="wait">
            {isProcessing ? (
              <motion.div
                key="processing"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex items-center justify-center gap-2 text-sm text-blue-600 dark:text-blue-400"
              >
                <motion.div
                  animate={{ rotate: [0, 360] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  <Sparkles size={16} />
                </motion.div>
                <span className="font-medium">AI is thinking... Click stop to interrupt</span>
              </motion.div>
            ) : (
              <motion.div
                key="idle"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="text-xs text-gray-500 dark:text-gray-400"
              >
                Press <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">Enter</kbd> to send, 
                <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono ml-1">Shift+Enter</kbd> for new line
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </motion.div>
  )
} 