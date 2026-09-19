import { app, BrowserWindow, session } from 'electron'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let miniWindow
let isQuitting = false

function createMiniWindow() {
  miniWindow = new BrowserWindow({
    width: 380,
    height: 560,
    minWidth: 320,
    minHeight: 420,
    maxWidth: 480,
    maxHeight: 720,
    backgroundColor: '#090909',
    autoHideMenuBar: true,
    alwaysOnTop: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  })

  miniWindow.on('close', (event) => {
    if (!isQuitting) {
      event.preventDefault()
      miniWindow.hide()
    }
  })

  if (app.isPackaged) {
    miniWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  } else {
    miniWindow.loadURL('http://localhost:5173')
  }
}

app.whenReady().then(() => {
  const isTrustedRenderer = (url) =>
    app.isPackaged
      ? url.startsWith('file://')
      : url.startsWith('http://localhost:5173')

  session.defaultSession.setPermissionCheckHandler(
    (webContents, permission) =>
      permission === 'media' && isTrustedRenderer(webContents.getURL()),
  )

  session.defaultSession.setPermissionRequestHandler(
    (webContents, permission, callback) => {
      callback(
        permission === 'media' && isTrustedRenderer(webContents.getURL()),
      )
    },
  )

  createMiniWindow()

  app.on('activate', () => {
    if (!miniWindow || miniWindow.isDestroyed()) {
      createMiniWindow()
    } else {
      miniWindow.show()
      miniWindow.focus()
    }
  })
})

app.on('before-quit', () => {
  isQuitting = true
})