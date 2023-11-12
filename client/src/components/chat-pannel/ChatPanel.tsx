import {useContext, useRef} from "preact/compat";
import Context from '../../utils/Context';
import * as ScrollArea from '@radix-ui/react-scroll-area';
import './styleChatPanel.css';
import useAuth from "../../hooks/UseAuth.tsx";
import useConversationMessagesPag from "../../hooks/UseConversationMessagesPag.tsx";
import {ConversationGet, ConversationMessage, MessageType, StateReduced, UserGet, UserInReview} from "../../api";
import ChatMessage from "./ChatMessage.tsx";
import {Text} from "@radix-ui/themes";
import {useEffect, useState} from "react";
import UploadDialog from "./UploadDialog.tsx";
import ReviewDialog from "./ReviewDialog.tsx";

function ChatPanel() {

    const {
        userApi,
        messageApi,
        reviewApi
    } = useContext(Context);

    const {
        currentUser
    } = useAuth();

    const {
        setOffset,
        messages,
        setMessages,
        selectedConversation
    } = useConversationMessagesPag(16);

    const [selector, setSelector] = useState<MessageType | null>(null);
    const [file, setFile] = useState<File | null>(null);
    const ref = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        setSelector(null);
        setFile(null);
    }, [selectedConversation]);

    const onSend = async () => {
        if (ref.current?.value === "" || !selectedConversation || !ref.current) {
            return;
        }
        if (selector && currentUser?.user_id !== selectedConversation?.customer_id) {
            setSelector(null);
            return;
        }
        if (file) {
            const result = await messageApi.postConversationMessageConversationConversationIdMessageMediaPost(
                selectedConversation?.conversation_id,
                ref.current?.value,
                file);
            if (result.status === 201) {
                setMessages([result.data, ...messages]);
                ref.current.value = "";
                setFile(null);
            }
        } else {
            const result = await messageApi.postConversationMessageConversationConversationIdMessagePost(
                selectedConversation?.conversation_id,
                ref.current?.value);
            if (result.status === 201) {
                console.log(result.data)
                setMessages([result.data, ...messages]);
                ref.current.value = "";
            }
        }
        if (selector === MessageType.AcceptQuoteMessage) {
            const result = await messageApi.postConversationMessageAndQuoteChangeConversationConversationIdMessageQuotePost(
                selectedConversation?.conversation_id,
                "Angebot angenommen",
                StateReduced.Accepted);
            if (result.status === 201) {
                setMessages([result.data, ...messages]);
                ref.current.value = "";
                setSelector(null);
            }
        }
        if (selector === MessageType.RejectQuoteMessage) {
            const result = await messageApi.postConversationMessageAndQuoteChangeConversationConversationIdMessageQuotePost(
                selectedConversation?.conversation_id,
                "Angebot abgelehnt",
                StateReduced.Rejected);
            if (result.status === 200) {
                setMessages([result.data, ...messages]);
                ref.current.value = "";
                setSelector(null);
            }
        }
    }

    const getCorrectUser = (selectedConversation: ConversationGet, currentUser: UserGet, message: ConversationMessage): {
        user_id: number,
        user: UserInReview,
        profile_picture: any
    } => {
        if (selectedConversation.customer_id === currentUser.user_id && message.sender_type === "customer" ||
            selectedConversation.service_provider_id === currentUser.user_id && message.sender_type === "service_provider") {
            return {user_id: currentUser.user_id, user: currentUser, profile_picture: null}
        } else {
            return {
                user_id: selectedConversation.customer_id === currentUser.user_id ? selectedConversation.service_provider_id : selectedConversation.customer_id,
                user: selectedConversation.customer_id === currentUser.user_id ? selectedConversation.service_provider : selectedConversation.customer,
                profile_picture: null
            }
        }
    }
    //Iterate through messages and add a line if the message is from another user
    let res = [];
    let bool = false;
    for (let i = messages.length - 1; i >= 0; i--) {
        if (!selectedConversation || !currentUser || !messages) {
            break;
        }
        const message = messages[i];
        const user = getCorrectUser(selectedConversation as ConversationGet, currentUser as UserGet, message);
        if (user.user_id !== currentUser.user_id && message.read_at === null && !bool) {
            res.push(
                <div style={{display: "flex", alignItems: "center", gap: "10px"}}>
                    <div style={{
                        height: "2px",
                        width: "85%",
                        backgroundColor: "var(--violet-9)"
                    }}/>
                    <Text weight={"bold"} style={{fontSize: "10pt", color: "var(--violet-9)", margin: 0}}>Neu</Text>
                </div>)
            bool = true;
        }
        res.push(
            <>
                <div style={{marginTop: "15px", marginBottom: "15px"}}>
                    <ChatMessage
                        key={message.message_id}
                        currentUser={currentUser as UserGet}
                        conversation={selectedConversation as ConversationGet}
                        message={message}
                        userApi={userApi}
                        messageApi={messageApi}
                    />
                </div>
            </>
        )
    }
    res = res.reverse();
    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <div className="chat-panel-view" width={"300px"}>
                <ScrollArea.Root className="ScrollAreaRoot">
                    <ScrollArea.Viewport id={"ScrollAreaViewportID_2"} className="ScrollAreaViewport" onScroll={() =>
                        setOffset(Math.abs(document.getElementById("ScrollAreaViewportID_2")!.scrollHeight - document.getElementById("ScrollAreaViewportID_2")!.scrollTop - document.getElementById("ScrollAreaViewportID_2")!.clientHeight) < 1)}>
                        {selectedConversation && currentUser && messages && res}
                    </ScrollArea.Viewport>
                    <ScrollArea.Scrollbar className="ScrollAreaScrollbar" orientation="vertical">
                        <ScrollArea.Thumb className="ScrollAreaThumb"/>
                    </ScrollArea.Scrollbar>
                    <ScrollArea.Scrollbar className="ScrollAreaScrollbar" orientation="horizontal">
                        <ScrollArea.Thumb className="ScrollAreaThumb"/>
                    </ScrollArea.Scrollbar>
                    <ScrollArea.Corner className="ScrollAreaCorner"/>
                </ScrollArea.Root>
            </div>
            <div style={{display: "flex", flexDirection: "row", justifyContent: "spaceEvenly"}}>
                <div
                    onClick={() => selector === MessageType.AcceptQuoteMessage ? setSelector(null) : setSelector(MessageType.AcceptQuoteMessage)}
                    style={{
                        margin: "5px",
                        padding: "5px",
                        borderRadius: "10px",
                        border: "2px solid var(--violet-7)",
                        backgroundColor: selector === MessageType.AcceptQuoteMessage ? "var(--violet-7)" : "transparent"
                    }}>
                    <Text>Accept Offer</Text></div>
                <div
                    onClick={() => selector === MessageType.RejectQuoteMessage ? setSelector(null) : setSelector(MessageType.RejectQuoteMessage)}
                    style={{
                        margin: "5px",
                        padding: "5px",
                        borderRadius: "10px",
                        border: "2px solid var(--violet-7)",
                        backgroundColor: selector === MessageType.RejectQuoteMessage ? "var(--violet-7)" : "transparent"
                    }}>
                    <Text>Reject Offer</Text></div>
                <div style={{
                    margin: "5px",
                    padding: "5px",
                    borderRadius: "10px",
                    border: "2px solid var(--violet-7)",
                    backgroundColor: file !== null ? "var(--violet-7)" : "transparent"
                }}>
                    <UploadDialog fileStorage={setFile}/></div>
                {selectedConversation && selectedConversation.state === "accepted" && currentUser &&
                    <div style={{
                        margin: "5px",
                        padding: "5px",
                        borderRadius: "10px",
                        border: "2px solid var(--violet-7)",
                        backgroundColor: file !== null ? "var(--violet-7)" : "transparent"
                    }}>
                        <ReviewDialog reviewAPI={reviewApi}
                                      conversation_id={selectedConversation.conversation_id}
                                      other_user_id={
                                          selectedConversation.customer_id === currentUser.user_id ? selectedConversation.service_provider_id : selectedConversation.customer_id
                                      }/>
                    </div>
                }
            </div>
            <div style={{display: selectedConversation?.state === "rejected" ? "none" : "flex", flexDirection: "row"}}>
                <div className="chat-view-search" height={"60px"}
                     style={{
                         backgroundColor: "white",
                         borderRadius: "5px",
                         zIndex: "10",
                         color: "black",
                         width: "95%"
                     }}>
                    <textarea ref={ref} style={{width: "100%", height: "30px", padding: "5px"}}
                              placeholder="Write a message"/>
                </div>
                <button onClick={() => onSend()}
                        style={{backgroundColor: "transparent", width: "10px", margin: "0 10px"}}>
                    <svg
                        width="30"
                        height="25"
                        viewBox="0 0 30 25"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M0.669987 24.1792L28.7 12.5L0.669991 0.820829L2.93515 12.404L2.95391 12.4999L2.93515 12.5959L0.669987 24.1792Z"
                            stroke="white"
                        />
                        <path d="M3 12.5L28 12.5" stroke="white"/>
                    </svg>
                </button>
            </div>
        </div>
    )
}

export default ChatPanel;