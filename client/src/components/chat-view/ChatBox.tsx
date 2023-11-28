import {ConversationGet, UserApi, UserGet, UserInReview} from "../../api";
import {useEffect, useState} from "react";
import * as Avatar from "@radix-ui/react-avatar";
import {Flex, Text} from "@radix-ui/themes";
import useAuth from "../../hooks/UseAuth.tsx";

interface ChatProps {
    currentUser: UserGet | null;
    selectedConversationId: number | null;
    conversation: ConversationGet;
    userApi: UserApi
}

function ChatBox(props: ChatProps) {

    const {isAuthenticated} = useAuth();

    const {currentUser, selectedConversationId, conversation, userApi} = props;

    if (currentUser === null) {
        return <div>"Not logged in"</div>
    }

    const [other_user_id,] = useState<number>(conversation.customer_id === currentUser.user_id ? conversation.service_provider_id : conversation.customer_id)
    const [other_user,] = useState<UserInReview>(conversation.customer_id === currentUser.user_id ? conversation.service_provider : conversation.customer);
    const [profile_picture, setProfilePicture] = useState<any>(null);

    useEffect(() => {
        if (!isAuthenticated) {
            return;
        }
        userApi.getImageUserIdImageGet(other_user_id, {responseType: 'blob'}).then(response => {
            if (response.status === 200) {
                // @ts-ignore
                setProfilePicture(URL.createObjectURL(response.data))
            }
        })
    }, [other_user_id, isAuthenticated])

    const formatTime = (date: Date) => {
        if (date.toString() === "Invalid Date") {
            return " -- ";
        }
        // Format the time as in WhatsApp
        if (date.getTime() >= (new Date().getTime() - 24 * 60 * 60 * 1000)) {
            const hours = date.getHours();
            const minutes = date.getMinutes();
            const ampm = hours >= 12 ? 'PM' : 'AM';
            const formattedHours = hours % 12;
            const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;
            return `${formattedHours}:${formattedMinutes} ${ampm}`;
        }
        if (date.getTime() >= (new Date().getTime() - 24 * 60 * 60 * 1000)) {
            return 'Yesterday';
        }
        if (date.getTime() >= (new Date().getTime() - 24 * 60 * 60 * 1000 * 7)) {
            return `${date.toLocaleString('default', {weekday: 'short'})}`
        }
        return `${date.getMonth()}/${date.getFullYear()}`
    }


    return (
        <div style={{
            width: "100%",
            display: "flex",
            gap: "10px",
            backgroundColor: selectedConversationId == conversation.conversation_id ? "var(--violet-1)" : "transparent",
        }}>
            <div className={"profile-picture"}>
                <Avatar.Root className="AvatarRoot">
                    <Avatar.Image
                        className="AvatarImage"
                        src={profile_picture}
                        alt="Colm Tuite"
                    />
                    <Avatar.Fallback className="AvatarFallback" delayMs={600}>
                        CT
                    </Avatar.Fallback>
                </Avatar.Root>
            </div>
            <div className={"chat-box-text-container"}>
                <Flex direction={"column"} width={"100%"}>
                    <div style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "space-between",
                        alignItems: "center"
                    }}>
                        <Text size={"3"} weight={"bold"}>{`${other_user.first_name} ${other_user.last_name}`}</Text>
                        {conversation.unread_messages > 0 && conversation.conversation_id !== selectedConversationId &&
                            <div style={{
                                borderRadius: "10px",
                                height: "15px",
                                width: "25px",
                                backgroundColor: "var(--violet-11)",
                                display: "flex",
                                flexDirection: "row",
                                alignItems: "center",
                                justifyContent: "center"
                            }}>
                                <label>{conversation.unread_messages}</label>
                            </div>
                        }
                    </div>
                    <div style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "space-between",
                        alignItems: "center",
                        maxWidth: "100%"
                    }}>
                        <Text size={"1"}
                              color={conversation.unread_messages > 0 && conversation.conversation_id !== selectedConversationId ? "white" : "gray"}
                              weight={conversation.unread_messages > 0 && conversation.conversation_id !== selectedConversationId ? "bold" : "normal"}
                              style={{
                                  whiteSpace: "nowrap",
                                  overflow: "hidden",
                                  textOverflow: "ellipsis",
                                  maxWidth: "80%"
                              }}
                        >{conversation.last_message?.text ?? "System: Ihr Auftrag wurde zugestellt"}</Text>

                        <Text size={"1"}
                              color={conversation.unread_messages > 0 && conversation.conversation_id !== selectedConversationId ? "white" : "gray"}
                              weight={conversation.unread_messages > 0 && conversation.conversation_id !== selectedConversationId ? "bold" : "normal"}
                              style={{whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis"}}
                        >{formatTime(new Date(conversation.last_message?.created_at as string))}</Text>
                    </div>
                    <div style={{display: "flex", flexDirection: "row", marginTop: "5px", gap: "10px"}}>
                        <div style={{
                            backgroundColor: "var(--violet-11)",
                            width: "100%",
                            height: "4px",
                            borderRadius: "3px"
                        }}/>
                        <div style={{
                            backgroundColor: conversation.last_message ? "var(--violet-11)" : "white",
                            width: "100%",
                            height: "4px",
                            borderRadius: "3px"
                        }}/>
                        <div style={{
                            backgroundColor: conversation.state === 'rejected' ? "var(--red-11)" :
                                conversation.state === 'accepted' ? "var(--violet-11)" : "white",
                            width: "100%",
                            height: "4px",
                            borderRadius: "3px"
                        }}/>
                    </div>
                </Flex>
            </div>
        </div>
    )
}

export default ChatBox;
