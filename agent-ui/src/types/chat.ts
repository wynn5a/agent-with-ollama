export interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
  status?: 'sending' | 'sent' | 'error'
  executionTime?: number
  thinking?: string
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}

export interface AgentStatus {
  isConnected: boolean
  isProcessing: boolean
  model: string
  endpoint: string
  lastPing?: Date
}

export interface AgentConfig {
  model: string
  endpoint: string
  temperature: number
  maxTokens: number
  verbose: boolean
} 