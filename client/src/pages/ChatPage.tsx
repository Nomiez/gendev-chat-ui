import ChatView from "../components/chat-view/ChatView.tsx";
import ChatPanel from "../components/chat-pannel/ChatPanel.tsx";

function ChatPage() {
    return (
        <main>
            <div style={{display: "flex", width: "100vw", height: "100vh"}}>
                <ChatView/>
                <ChatPanel/>
            </div>
        </main>
    );
}

export default ChatPage;