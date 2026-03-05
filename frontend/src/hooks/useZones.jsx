import { useState, useEffect } from 'react'

export function useZones(zone_num) {
    const [data,    setData]    = useState(null)
    const [loading, setLoading] = useState(null)
    const [error,   setError]   = useState(null)

    const url = `http://127.0.0.1:8000/hvac/api/`

    async function PostData(zone_id, point_name, data){
        const options = {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify({ [point_name] : data })
        }

        const response = await fetch(`${url}zone/${zone_id}/`, options)
        if (!response.ok) throw new Error(
            setError(response)
        )
    }

    useEffect(() => {
        let cancelled = false

        const fetchData = async () => {
            try {
                setLoading(true)
                setError(null)
                const response = await fetch(`${url}zones/`)
                if (!response.ok) throw new Error(`HTTP ERROR: STATUS: ${response.status}`)
                const result = await response.json()
                if (!cancelled) setData(result)
            } catch (err) {
                if (!cancelled) setError(err.message)
            } finally {
                if (!cancelled) setLoading(false)
            }
        }

        fetchData()
        const interval = setInterval(fetchData, 3000)
        return () => {
            cancelled = true
            clearInterval(interval)
        }
    }, [url, zone_num])

    return { data, loading, error, PostData }
}
