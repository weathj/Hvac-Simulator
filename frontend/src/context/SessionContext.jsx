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

    return (
        <SessionContext.Provider value={{ session_id }}>
            {children}
        </SessionContext.Provider>
    )
}

export function useSessionContext() {
    return useContext(SessionContext)
}
