import {useEffect, useState} from "react";
import {EventSourcePolyfill} from "event-source-polyfill";
import useAuth from "./UseAuth.tsx";

function UseSSE() {

    const [data, setData] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [eventSource, setEventSource] = useState<EventSourcePolyfill | null>(null);

    const [token, setToken] = useState<string | null>();


    const {
        getTokenSilently,
    } = useAuth();

    useEffect(() => {
        const wrapper = async () => {
            setToken(await getTokenSilently());
        }
        wrapper();
    }, [])


    const connect = () => {
        const eventSource = new EventSourcePolyfill('api/stream',
            {
                headers: {
                    'Authorization': 'Bearer ' + token,
                }
            });
        setEventSource(eventSource);
    };

    const close = () => {
        if (eventSource)
            eventSource.close();
    };

    useEffect(() => {
        if (!eventSource) return;

        eventSource.onmessage = (e) => {
            setData(JSON.stringify({id: Math.random().toString(), message: e.data}));
        };

        eventSource.onerror = (e) => {
            setError(e.type);
        };

        return () => {
            eventSource.close();
        };
    }, [eventSource]);

    return {data, error, connect, close};
}

export default UseSSE;