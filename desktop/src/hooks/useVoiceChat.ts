import { useRef, useState } from 'react'
import { sendVoiceRecording } from '../services/voice'

export type VoiceStatus = 'idle' | 'recording' | 'sending' | 'error'

export function useVoiceChat() {
  const [voiceStatus, setVoiceStatus] = useState<VoiceStatus>('idle')
  const recorderRef = useRef<MediaRecorder | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const chunksRef = useRef<Blob[]>([])

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      })

      const recorder = new MediaRecorder(stream)

      streamRef.current = stream
      recorderRef.current = recorder
      chunksRef.current = []

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      recorder.onstop = async () => {
        streamRef.current?.getTracks().forEach((track) => track.stop())
        streamRef.current = null
        recorderRef.current = null

        const recording = new Blob(chunksRef.current, {
          type: recorder.mimeType,
        })

        setVoiceStatus('sending')

        try {
          const audioUrl = await sendVoiceRecording(recording)
          const audio = new Audio(audioUrl)

          audio.onended = () => URL.revokeObjectURL(audioUrl)
          await audio.play()

          setVoiceStatus('idle')
        } catch (error) {
          console.error('Unable to complete voice chat.', error)
          setVoiceStatus('error')
        }
      }

      recorder.start()
      setVoiceStatus('recording')
    } catch (error) {
      console.error('Unable to access the microphone.', error)
      setVoiceStatus('error')
    }
  }

  function stopRecording() {
    if (recorderRef.current?.state === 'recording') {
      recorderRef.current.stop()
    }
  }

  function toggleRecording() {
    if (voiceStatus === 'recording') {
      stopRecording()
      return
    }

    if (voiceStatus === 'idle' || voiceStatus === 'error') {
      void startRecording()
    }
  }

  return {
    toggleRecording,
    voiceStatus,
  }
}