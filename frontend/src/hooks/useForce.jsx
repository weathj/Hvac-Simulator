import { useState, useEffect } from 'react'

export function useForce() {
    const [loading, setLoading] = useState(false)
    const [error, setError]     = useState(null)
    const [success, setSuccess] = useState(false)

    const post = async (url, field, value) => {
        setLoading(true)
        setError(null)
        setSuccess(false)
        try {
            await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ [field]: value }),
        })
            setSuccess(true)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return { post, loading, error, success }
}