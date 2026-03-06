import { useState, useEffect } from 'react'

export function useAHU() {
    const [ data, setData ] = useState(null);
    const [ loading, setLoading ] = useState(null);
    const [ error, setError ] = useState(null);

    const url = "http://localhost:8000/hvac/api/airunit/"

    async function PostData(point_name, data){
        const options = {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify({ [point_name] : data })
        }

        const response = await fetch(`${url}`, options)
        if (!response.ok) throw new Error(
            setError(response)
        )
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
    }

    fetchData();
    const interval = setInterval(fetchData, 3000);

    return () => {
        cancelled = true;
        clearInterval(interval);
    }
    }, [url]);

    return { data, loading, error, PostData };
}