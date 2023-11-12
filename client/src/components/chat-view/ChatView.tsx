import {useContext} from "preact/compat";
import Context from '../../utils/Context';
import * as ScrollArea from '@radix-ui/react-scroll-area';
import './styleChatView.css';
import './styleAvatar.css';
import useAuth from "../../hooks/UseAuth.tsx";
import useConversationPag from "../../hooks/UseConversationPag.tsx";
import ChatBox from "./ChatBox.tsx";

function ChatView() {

    const {
        selectedConversation,
        setSelectedConversation,
        userApi,
    } = useContext(Context);

    const {
        currentUser
    } = useAuth();

    const {
        conversations,
        setOffset
    } = useConversationPag(20);

    return (
        <div className="chat-view" width={"300px"}>
            <ScrollArea.Root className="ScrollAreaRoot">
                <ScrollArea.Viewport id={"ScrollAreaViewportID"} className="ScrollAreaViewport" onScroll={() =>
                    setOffset(Math.abs(document.getElementById("ScrollAreaViewportID")!.scrollHeight - document.getElementById("ScrollAreaViewportID")!.scrollTop - document.getElementById("ScrollAreaViewportID")!.clientHeight) < 1)}>
                    <div style={{padding: "15px"}}>
                        {conversations.map((conversation) => {
                            return (
                                <>
                                    <div style={{marginTop: "15px", marginBottom: "15px"}}
                                         onClick={() => setSelectedConversation(conversation)}>
                                        <ChatBox
                                            key={conversation.conversation_id}
                                            currentUser={currentUser}
                                            selectedConversationId={selectedConversation ? selectedConversation.conversation_id : null}
                                            conversation={conversation}
                                            userApi={userApi}/>
                                    </div>
                                    <div style={{height: "1px", width: "100%", backgroundColor: "gray"}}/>
                                </>
                            )
                        })}
                    </div>
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
    )
}

export default ChatView;