import {useMemo, useState} from 'react';
import Context from './Context';
import {
    Configuration,
    ConfigurationParameters,
    ConversationApi,
    MessageApi,
    UserApi,
    ReviewApi,
    StreamApi,
    ConversationGet,
    TokenApi,
} from '../api';
import {ReactNode, useEffect} from "preact/compat";
import useAuth from "../hooks/UseAuth.tsx";

/**
 * Sets Context for its children
 * @param  {{ children: ReactNode }} props
 * @return {JSX.Element}
 */
function ContextWrapper(props: { children: ReactNode }) {
    const {children} = props;

    const [configuration, setConfiguration] = useState<Configuration>(new Configuration());

    const {
        getTokenSilently,
        isAuthenticated
    } = useAuth()

    useEffect(() => {
        async function initConfiguration() {
            if (!isAuthenticated) {
                return;
            }
            const token = await getTokenSilently();
            if (!token) {
                return;
            }
            const parameters: ConfigurationParameters = {}
            parameters.basePath = "api"
            parameters.accessToken = token;
            setConfiguration(new Configuration(parameters));
        }

        initConfiguration();
    }, [isAuthenticated])

    const conversationApi = useMemo(() => new ConversationApi(configuration), [
        configuration],
    );

    const messageApi = useMemo(() => new MessageApi(configuration), [
        configuration,
    ]);

    const userApi = useMemo(() => new UserApi(configuration), [
        configuration,
    ]);

    const reviewApi = useMemo(() => new ReviewApi(configuration), [
        configuration,
    ]);

    const streamApi = useMemo(() => new StreamApi(configuration), [
        configuration,
    ]);

    const tokenApi = useMemo(() => new TokenApi(configuration), [
        configuration,
    ]);

    const [conversations, setConversations] = useState<
        ConversationGet[]
    >([]);

    const [selectedConversation, setSelectedConversation] = useState<
        ConversationGet | null
    >(null);

    const valueWrapper = useMemo(
        () => ({
            conversations,
            setConversations,
            selectedConversation,
            setSelectedConversation,
            conversationApi,
            messageApi,
            userApi,
            reviewApi,
            streamApi,
            tokenApi,
            configuration
        }), [conversations, selectedConversation, conversationApi, messageApi, userApi, reviewApi, streamApi, tokenApi, configuration]
    );

    return <Context.Provider value={valueWrapper}>{children}</Context.Provider>;
}

export default ContextWrapper;
