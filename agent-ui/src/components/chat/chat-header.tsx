'use client'

import { motion } from 'framer-motion'
import { Bot, Settings, Wifi, WifiOff, Clock, Sparkles } from 'lucide-react'
import { AgentStatus } from '@/types/chat'
import { cn } from '@/lib/utils'

interface ChatHeaderProps {
  status: AgentStatus
  onSettingsClick?: () => void
  messageCount?: number
}

export function ChatHeader({ status, onSettingsClick, messageCount = 0 }: ChatHeaderProps) {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="glass-morphism sticky top-0 z-50 border-b border-white/10"
    >
      <div className="max-w-5xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left side - Agent info */}
          <div className="flex items-center gap-4">
            <motion.div 
              className="relative"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 400, damping: 17 }}
            >
              <div className="w-12 h-12 bg-gradient-to-br from-violet-500 via-purple-500 to-blue-500 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-purple-500/25">
                <motion.div
                  animate={status.isProcessing ? { rotate: [0, 360] } : {}}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  <Bot size={24} />
                </motion.div>
              </div>
              
              {/* Enhanced status indicator */}
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className={cn(
                  "absolute -bottom-1 -right-1 w-5 h-5 rounded-full border-2 border-white shadow-lg",
                  status.isConnected 
                    ? "bg-emerald-500" 
                    : "bg-red-500"
                )}
              >
                {status.isProcessing && (
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1, repeat: Infinity }}
                    className="w-full h-full rounded-full bg-blue-500"
                  />
                )}
              </motion.div>
            </motion.div>

            <div className="flex flex-col">
              <motion.h1 
                className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                AI Agent Assistant
              </motion.h1>
              
              <motion.div 
                className="flex items-center gap-3 text-sm"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
              >
                {status.isConnected ? (
                  <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
                    <Wifi size={14} />
                    <span className="font-medium">Online</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-1.5 text-red-500">
                    <WifiOff size={14} />
                    <span className="font-medium">Offline</span>
                  </div>
                )}
                
                {status.isProcessing && (
                  <motion.div 
                    className="flex items-center gap-1.5 text-blue-500"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                  >
                    <motion.div
                      animate={{ rotate: [0, 360] }}
                      transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                    >
                      <Sparkles size={14} />
                    </motion.div>
                    <span className="font-medium">Thinking...</span>
                  </motion.div>
                )}
              </motion.div>
            </div>
          </div>

          {/* Right side - Stats and controls */}
          <div className="flex items-center gap-6">
            {/* Message count */}
            {messageCount > 0 && (
              <motion.div 
                className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-white/50 dark:bg-black/20 rounded-full text-sm font-medium text-gray-700 dark:text-gray-300"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 }}
              >
                <Clock size={14} />
                <span>{messageCount} messages</span>
              </motion.div>
            )}

            {/* Model info */}
            <motion.div 
              className="hidden md:flex flex-col items-end text-xs"
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <span className="font-semibold text-gray-900 dark:text-white">{status.model}</span>
              <span className="text-gray-500 dark:text-gray-400">{status.endpoint}</span>
            </motion.div>

            {/* Settings button */}
            <motion.button
              onClick={onSettingsClick}
              className="p-3 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors rounded-xl hover:bg-white/50 dark:hover:bg-black/20"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6 }}
            >
              <Settings size={20} />
            </motion.button>
          </div>
        </div>

        {/* Enhanced status bar */}
        <motion.div 
          className="mt-4 h-1.5 bg-gray-200/50 dark:bg-gray-700/50 rounded-full overflow-hidden"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 0.7, duration: 0.8 }}
        >
          <motion.div
            className={cn(
              "h-full rounded-full",
              status.isConnected 
                ? "bg-gradient-to-r from-emerald-500 to-blue-500" 
                : "bg-gradient-to-r from-red-500 to-orange-500"
            )}
            initial={{ width: "0%" }}
            animate={{ 
              width: status.isConnected ? "100%" : "30%",
              opacity: status.isProcessing ? [1, 0.6, 1] : 1
            }}
            transition={{ 
              width: { duration: 1, ease: "easeOut" },
              opacity: { duration: 1.5, repeat: status.isProcessing ? Infinity : 0 }
            }}
          />
        </motion.div>
      </div>
    </motion.header>
  )
} 