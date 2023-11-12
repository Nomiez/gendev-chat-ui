import {useContext, useEffect} from "preact/compat";
import context from "../utils/Context.tsx";
import {useState} from "react";
import {ConversationMessage} from "../api";

function UseConversationPag(sizeProp: number) {


    const [page, setPage] = useState<number>(1);
    const [size, setSize] = useState<number>(sizeProp);
    const [offset, setOffset] = useState<boolean>(false);
    const [messages, setMessages] = useState<ConversationMessage[]>([]);

    const {
        selectedConversation,
        messageApi,
    } = useContext(context);


    // Fetch conversations every 10 seconds
    // TODO: Use SSE instead
    useEffect(() => {
        const interval = setInterval(async () => {
            if (selectedConversation !== null) {
                const response = await messageApi.getConversationMessagePagConversationConversationIdMessageGet(selectedConversation.conversation_id, page, size);
                if (response.status === 200) {
                    if (response.data[0].message_id !== messages[0].message_id) {
                        setMessages(response.data);
                    }
                }
            }
            console.log("fetching messages")
        }, 1000);
        return () => clearInterval(interval);

    }, [messageApi, selectedConversation])


    useEffect(() => {
        const loadConversationMessages = async (page: number, size: number) => {
            if (!selectedConversation) {
                return [];
            }
            const response = await
                messageApi.getConversationMessagePagConversationConversationIdMessageGet(selectedConversation?.conversation_id, page, size);
            if (response.status === 200) {
                return response.data;
            } else {
                return [];
            }
        }

        const asyncWrapper = async () => {
            if (!selectedConversation) {
                return;
            }
            const newMessages = await loadConversationMessages(page, size);
            setMessages(newMessages);
            setPage(1);
            setSize(sizeProp)
        }
        asyncWrapper();

    }, [selectedConversation])

    useEffect(() => {
        console.log("offset: " + offset)
        if (offset) {
            const loadConversationMessages = async (page: number, size: number) => {
                if (!selectedConversation) {
                    return [];
                }
                const response = await
                    messageApi.getConversationMessagePagConversationConversationIdMessageGet(selectedConversation?.conversation_id, page, size);
                if (response.status === 200) {
                    return response.data;
                } else {
                    return [];
                }
            }

            const asyncWrapper = async () => {
                if (!selectedConversation) {
                    return [];
                }
                const newMessages = await loadConversationMessages(page + 1, size);
                if (newMessages.length === 0) {
                    return [];
                }
                setMessages(prevState => [...prevState, ...newMessages]);
                setPage(prev => prev + 1);
                setSize(prev => prev)
            }
            console.log("offset: " + offset);
            asyncWrapper();
        }
    }, [offset])

    return {
        messages,
        page,
        setOffset,
        selectedConversation,
        setMessages
    };
}

export default UseConversationPag;