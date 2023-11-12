import {createContext} from 'preact';
import {
    Configuration,
    ConversationApi,
    MessageApi,
    UserApi,
    ReviewApi,
    StreamApi,
    ConversationGet,
    TokenApi
} from '../api';
import {StateUpdater} from "preact/hooks";

/* init context */
const Context = createContext<{
    conversations: ConversationGet[];
    setConversations: StateUpdater<ConversationGet[]>;

    selectedConversation: ConversationGet | null;
    setSelectedConversation: StateUpdater<ConversationGet | null>;

    conversationApi: ConversationApi,
    messageApi: MessageApi,
    userApi: UserApi
    reviewApi: ReviewApi
    streamApi: StreamApi
    tokenApi: TokenApi
    configuration: Configuration;
}>({
    conversations: [],
    setConversations: () => {
    },
    selectedConversation: null,
    setSelectedConversation: () => {
    },
    conversationApi: new ConversationApi(),
    messageApi: new MessageApi(),
    userApi: new UserApi(),
    reviewApi: new ReviewApi(),
    streamApi: new StreamApi(),
    tokenApi: new TokenApi(),
    configuration: new Configuration()
});

export default Context;
