import {useContext, useEffect} from "preact/compat";
import context from "../utils/Context.tsx";
import {useState} from "react";
import {ConversationMessage} from "../api";
import useSSE from "./UseSSE.tsx";

function UseConversationMessagePag(sizeProp: number) {


    const [page, setPage] = useState<number>(1);
    const [size, setSize] = useState<number>(sizeProp);
    const [offset, setOffset] = useState<boolean>(false);
    const [messages, setMessages] = useState<ConversationMessage[]>([]);

    const {
        selectedConversation,
        messageApi,
    } = useContext(context);

    const {
        data,
        connect,
        close
    } = useSSE();

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
        connect();
        return () => {
            close();
        }
    }, [selectedConversation])

    useEffect(() => {
        console.log("data: " + data)
        const wrapper = async (data: any) => {
            console.log(data);
            if (selectedConversation !== null) {
                const response = await messageApi.getConversationMessagePagConversationConversationIdMessageGet(selectedConversation.conversation_id, 1, size * page);
                if (response.status === 200) {
                    if (messages && messages.length > 0 && response.data[0].message_id !== messages[0].message_id) {
                        setMessages(response.data);
                        setPage(1);
                        setSize(size * page);
                    }
                }
            }
        }

        if (data) {
            wrapper(data);
        }

    }, [data])


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

export default UseConversationMessagePag;