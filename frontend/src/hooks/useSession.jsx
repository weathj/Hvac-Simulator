import { useState, useEffect } from 'react'

export function useSession() {
    const [ data, setData ] = useState(null);
    const [ loading, setLoading ] = useState(null);
    const [ error, setError ] = useState(null);
    const [ session_id, setSessionId ] = useState(null);

    const url = `${import.meta.env.VITE_API_URL}/hvac/api/create/`

    async function CreateSession(){
        const options = {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify({ 'session-type' : 'new' })
        }
        const response = await fetch(url, options)
        if (!response.ok) {
            setError(response)
            return
        }
        const result = await response.json()
        setSessionId(result.session_id)
    }

    useEffect(() => {
        let cancelled = false;

        const fetchData = async () => {
            try{
                setLoading(true);
                setError(null);
                const response = await fetch(url);

                if(!response.ok){
                    throw new Error(`HTTP ERROR: STATUS: ${response.status}`)
                }

                const result = await response.json();

                if(!cancelled){
                    setData(result);
                }
            }catch(err){
                if(!cancelled){
                    setError(err.message);
                }
            }finally{
                if(!cancelled){
                    setLoading(false);
                }
            }
        };

        fetchData();

        return () => {
            cancelled = true;
        };
    }, [url]);

    return { data, error, session_id, CreateSession };
}