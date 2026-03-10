import { useState } from 'react'

export function useSession() {
    const [ error, setError ] = useState(null);

    const url = `${import.meta.env.VITE_API_URL}/hvac/api/create/`

    async function CreateSession(){
        const options = {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify({ 'session-type' : 'new' })
        }    
            const response = await fetch(`${url}`, options)
            if (!response.ok) throw new Error(
                setError(response)
            )
    }

    return { error, CreateSession };
}