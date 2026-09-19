const API_BASE_URL = 'http://127.0.0.1:8000'

export async function sendVoiceRecording(recording: Blob): Promise<string> {
  const formData = new FormData()

  formData.append('file', recording, 'alab-recording.webm')

  const response = await fetch(`${API_BASE_URL}/voice-chat`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`Voice request failed with status ${response.status}`)
  }

  const audioResponse = await response.blob()

  return URL.createObjectURL(audioResponse)
}