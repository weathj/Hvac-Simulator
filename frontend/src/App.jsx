import Dashboard from './components/Dashboard'
import './App.css'
import { SessionProvider } from './context/SessionContext'

function App() {
  return (
    <SessionProvider>
      <Dashboard />
    </SessionProvider>
  )
}

export default App