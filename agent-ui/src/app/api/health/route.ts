import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Check if the Python backend is running
    const response = await fetch('http://localhost:8000/health', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (response.ok) {
      return NextResponse.json({ status: 'healthy', backend: 'connected' })
    } else {
      return NextResponse.json({ status: 'unhealthy', backend: 'disconnected' }, { status: 503 })
    }
  } catch (error) {
    return NextResponse.json({ 
      status: 'unhealthy', 
      backend: 'disconnected',
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 503 })
  }
} 