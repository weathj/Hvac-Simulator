import { useEffect } from 'react'
import Dashboard from './components/Dashboard'
import { useSession } from './hooks/useSession'
import './App.css'

function App() {
  const { CreateSession } = useSession()

  useEffect(() => {
    CreateSession()
  }, [])

  return (
    <Dashboard />
  )
}

export default App
