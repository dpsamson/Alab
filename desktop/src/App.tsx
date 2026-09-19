import { useState, type FormEvent } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
  }

  return (
    <main className="mini-window">
      <section className="initial-state" aria-label="Alab assistant">
        <div className="welcome-content">
          <h1 className="wordmark">Alab</h1>

          <p className="greeting-bubble">
            Hi, I’m Alab. How can I help with your job search today?
          </p>
        </div>
      </section>

      <form className="message-form" onSubmit={handleSubmit}>
        <div className="input-shell">
          <input
            aria-label="Message Alab"
            className="message-input"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Ask Alab anything..."
          />

          <button
            aria-label="Start voice input"
            className="microphone-button"
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