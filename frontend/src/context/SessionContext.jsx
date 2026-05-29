import { createContext, useContext, useEffect, useRef } from 'react'
import { useSession } from '../hooks/useSession'

const SessionContext = createContext(null)

export function SessionProvider({ children }) {
    const { session_id, CreateSession } = useSession()
    const called = useRef(false)

    useEffect(() => {
        if (!called.current) {
            CreateSession()
            called.current = true
        }
    }, [])

    useEffect(() => {
        const handleUnload = () => {
            if (session_id) {
                navigator.sendBeacon(`${import.meta.env.VITE_API_URL}/hvac/api/${session_id}/delete/`)
            }
        }

        window.addEventListener('beforeunload', handleUnload)
        return () => window.removeEventListener('beforeunload', handleUnload)
    }, [session_id])

    return (
        <SessionContext.Provider value={{ session_id }}>
            {children}
        </SessionContext.Provider>
    )
}

export function useSessionContext() {
    return useContext(SessionContext)
}
