import { useState, type FormEvent } from 'react'
import { sendChatMessage } from './services/chat'
import './App.css'

type ChatStatus = 'idle' | 'loading' | 'error'

function App() {
  const [message, setMessage] = useState('')
  const [lastQuestion, setLastQuestion] = useState('')
  const [reply, setReply] = useState('')
  const [chatStatus, setChatStatus] = useState<ChatStatus>('idle')
  const [hasMessages, setHasMessages] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedMessage = message.trim()

    if (!trimmedMessage || chatStatus === 'loading') {
      return
    }

    setLastQuestion(trimmedMessage)
    setMessage('')
    setHasMessages(true)
    setChatStatus('loading')
    setReply('')

    try {
      const chatReply = await sendChatMessage(trimmedMessage)
      setReply(chatReply)
      setChatStatus('idle')
    } catch (error) {
      console.error('Unable to reach the Alab backend.', error)
      setReply(
        'I couldn’t reach the Alab backend. Make sure the FastAPI server is running, then try again.',
      )
      setChatStatus('error')
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
            <p className="user-message">{lastQuestion}</p>

            <article
              aria-busy={chatStatus === 'loading'}
              className={`response-card ${chatStatus === 'error' ? 'is-error' : ''}`}
            >
              <p className="response-label">ALAB</p>

              {chatStatus === 'loading' ? (
                <p className="response-text loading-response">
                  <span className="loading-dot" />
                  Thinking…
                </p>
              ) : (
                <p className="response-text">{reply}</p>
              )}
            </article>
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
        <div className="input-shell">
          <input
            aria-label="Message Alab"
            className="message-input"
            disabled={chatStatus === 'loading'}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Ask Alab anything..."
          />

          <button
            aria-label="Start voice input"
            className="microphone-button"
            disabled={chatStatus === 'loading'}
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