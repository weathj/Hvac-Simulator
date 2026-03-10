import Dashboard from './components/Dashboard'
import { useSession } from './hooks/useSession'
import './App.css'

function App() {

  CreateSession()

  return (
    <Dashboard />
  )
}

export default App
