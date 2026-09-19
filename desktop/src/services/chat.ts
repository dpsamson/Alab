const API_BASE_URL = 'http://127.0.0.1:8000'

type ChatResponse = {
  reply?: string
}

export async function sendChatMessage(message: string): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`)
  }

  const payload = (await response.json()) as ChatResponse

  if (typeof payload.reply !== 'string') {
    throw new Error('The chat response did not include a reply.')
  }

  return payload.reply
}