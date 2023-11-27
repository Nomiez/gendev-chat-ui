import {useContext, useEffect} from "preact/compat";
import context from "../utils/Context.tsx";
import {useState} from "react";

function UseConversationPag(sizeProp: number) {


    const [page, setPage] = useState<number>(1);
    const [size, setSize] = useState<number>(sizeProp);
    const [offset, setOffset] = useState<boolean>(false);

    const {
        conversations,
        setConversations,
        conversationApi,
        setSelectedConversation,
        selectedConversation
    } = useContext(context);

    // Fetch conversations every 1 seconds
    // TODO: Use SSE instead
    useEffect(() => {
        const interval = setInterval(async () => {
            const response = await conversationApi.getConversationsPagConversationGet(1, page * size);
            if (response.status === 200) {
                let update = false;
                for (let i = 0; i < response.data.length; i++) {
                    if (conversations[i] && response.data[i].last_message?.message_id !== conversations[i].last_message?.message_id) {
                        update = true;
                        break;
                    }
                }
                if (update) {
                    setConversations(response.data);
                    console.log("TEST")
                }
                const newSelectedConversation = conversations.filter((conversation) => conversation.conversation_id === selectedConversation?.conversation_id)[0];
                if (newSelectedConversation && newSelectedConversation.last_message?.message_id !== selectedConversation?.last_message?.message_id) {
                    setSelectedConversation(newSelectedConversation);
                }
            }
        }, 1000);
        return () => clearInterval(interval);

    }, [conversationApi, selectedConversation, conversations, page, size])


    useEffect(() => {
        const loadConversations = async (page: number, size: number) => {
            const response = await conversationApi.getConversationsPagConversationGet(page, size);
            if (response.status === 200) {
                return response.data;
            } else {
                return [];
            }
        }

        const asyncWrapper = async () => {
            if (conversations.length > 0) {
                return;
            }
            const newConversations = await loadConversations(page, size);
            if (newConversations.length === 0) {
                return;
            }
            setConversations(newConversations);
            setPage(1);
            setSize(prev => prev)
        }
        asyncWrapper();

    }, [conversationApi])

    useEffect(() => {
        if (offset) {
            const loadConversations = async (page: number, size: number) => {
                const response = await conversationApi.getConversationsPagConversationGet(page, size);
                if (response.status === 200) {
                    return response.data;
                } else {
                    return [];
                }
            }

            const asyncWrapper = async () => {
                const newConversations = await loadConversations(page + 1, size);
                setConversations(prev => [...prev, ...newConversations]);
                console.log("newConversations: ", newConversations)
                setPage(prev => prev + 1);
                setSize(prev => prev)
            }
            asyncWrapper();
        }
    }, [offset])

    return {
        conversations,
        page,
        setOffset
    };
}

export default UseConversationPag;