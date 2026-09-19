import { useEffect, useRef, useState, type FormEvent } from 'react'
import {
  sendChatMessage,
  type ChatHistoryMessage,
} from './services/chat'
import './App.css'
import { useVoiceChat } from './hooks/useVoiceChat'

type MessageRole = 'user' | 'assistant'
type MessageStatus = 'complete' | 'loading' | 'error'

type ChatMessage = {
  id: string
  role: MessageRole
  content: string
  status: MessageStatus
}

function App() {
  const { toggleRecording, voiceStatus } = useVoiceChat()
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const conversationEndRef = useRef<HTMLDivElement>(null)

  const hasMessages = messages.length > 0
  const isLoading = messages.some((chatMessage) => chatMessage.status === 'loading')

  useEffect(() => {
    conversationEndRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'end',
    })
  }, [messages])

  function getCompletedHistory(): ChatHistoryMessage[] {
    return messages
      .filter((chatMessage) => chatMessage.status === 'complete')
      .map(({ role, content }) => ({ role, content }))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedMessage = message.trim()

    if (!trimmedMessage || isLoading) {
      return
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmedMessage,
      status: 'complete',
    }

    const pendingAssistantMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      status: 'loading',
    }

    const history = getCompletedHistory()

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
      pendingAssistantMessage,
    ])
    setMessage('')

    try {
      const reply = await sendChatMessage(trimmedMessage, history)

      setMessages((currentMessages) =>
        currentMessages.map((chatMessage) =>
          chatMessage.id === pendingAssistantMessage.id
            ? {
                ...chatMessage,
                content: reply,
                status: 'complete',
              }
            : chatMessage,
        ),
      )
    } catch (error) {
      console.error('Unable to reach the Alab backend.', error)

      setMessages((currentMessages) =>
        currentMessages.map((chatMessage) =>
          chatMessage.id === pendingAssistantMessage.id
            ? {
                ...chatMessage,
                content:
                  'I couldn’t reach the Alab backend. Make sure FastAPI is running, then try again.',
                status: 'error',
              }
            : chatMessage,
        ),
      )
    }
  }

  return (
    <main className={`mini-window ${hasMessages ? 'is-active' : ''}`}>
      {hasMessages ? (
        <section className="active-state" aria-label="Alab conversation">
          <header className="active-header">
            <h1 className="wordmark">Alab</h1>
          </header>

          <div className="conversation" aria-live="polite">
            {messages.map((chatMessage) =>
              chatMessage.role === 'user' ? (
                <p className="user-message" key={chatMessage.id}>
                  {chatMessage.content}
                </p>
              ) : (
                <article
                  aria-busy={chatMessage.status === 'loading'}
                  className={`response-card ${
                    chatMessage.status === 'error' ? 'is-error' : ''
                  }`}
                  key={chatMessage.id}
                >
                  <p className="response-label">ALAB</p>

                  {chatMessage.status === 'loading' ? (
                    <p className="response-text loading-response">
                      <span className="loading-dot" />
                      Thinking…
                    </p>
                  ) : (
                    <p className="response-text">{chatMessage.content}</p>
                  )}
                </article>
              ),
            )}

            <div ref={conversationEndRef} />
          </div>
        </section>
      ) : (
        <section className="initial-state" aria-label="Alab assistant">
          <div className="welcome-content">
            <h1 className="wordmark">Alab</h1>

            <p className="greeting-bubble">
              Hi, I’m Alab. How can I help with your job search today?
            </p>
          </div>
        </section>
      )}

      <form className="message-form" onSubmit={handleSubmit}>
        {voiceStatus !== 'idle' && (
        <p className="voice-status" aria-live="polite">
          {voiceStatus === 'recording' && 'Listening… click the mic to send.'}
          {voiceStatus === 'sending' && 'Sending voice message…'}
          {voiceStatus === 'error' && 'Microphone or voice request unavailable.'}
        </p>
      )}
        <div className="input-shell">
          <input
            aria-label="Message Alab"
            className="message-input"
            disabled={isLoading}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Ask Alab anything..."
          />

          <button
            aria-label= {
              voiceStatus === 'recording'
              ? 'Stop voice input'
              : 'Start voice input'
            }
            className={`microphone-button ${ voiceStatus === 'recording' ? 'is-recording' : ''
            }`}
            disabled={isLoading || voiceStatus === 'sending'}
            onClick = {toggleRecording}
            type="button"
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 14.5a3.5 3.5 0 0 0 3.5-3.5V6a3.5 3.5 0 1 0-7 0v5a3.5 3.5 0 0 0 3.5 3.5Z" />
              <path d="M18 11a6 6 0 0 1-12 0M12 17v4M8.5 21h7" />
            </svg>
          </button>
        </div>
      </form>
    </main>
  )
}

export default App