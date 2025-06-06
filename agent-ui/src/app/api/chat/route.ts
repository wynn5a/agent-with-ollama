import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json()

    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Message is required and must be a string' },
        { status: 400 }
      )
    }

    // Connect to your Python backend
    // Replace this URL with your actual Python server endpoint
    const pythonBackendUrl = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000'
    
    const response = await fetch(`${pythonBackendUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message,
        timestamp: new Date().toISOString()
      }),
      // Add timeout
      signal: AbortSignal.timeout(120000), // 2 minutes timeout
    })

    if (!response.ok) {
      throw new Error(`Python backend responded with status: ${response.status}`)
    }

    const data = await response.json()
    
    return NextResponse.json({
      response: data.response || data.result || 'No response from agent',
      executionTime: data.executionTime,
      thinking: data.thinking,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Chat API error:', error)
    
    if (error instanceof Error) {
      if (error.name === 'AbortError' || error.message.includes('timeout')) {
        return NextResponse.json(
          { error: 'Request timeout - the agent took too long to respond' },
          { status: 408 }
        )
      }
      
      if (error.message.includes('ECONNREFUSED') || error.message.includes('fetch failed')) {
        return NextResponse.json(
          { error: 'Cannot connect to AI agent. Please make sure the Python backend is running.' },
          { status: 503 }
        )
      }
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'AI Agent Chat API is running',
    timestamp: new Date().toISOString(),
    endpoints: {
      chat: 'POST /api/chat'
    }
  })
} 