import {ConversationGet, ConversationMessage, MessageApi, UserApi, UserGet, UserInReview} from "../../api";
import {useEffect, useState} from "react";
import * as Avatar from "@radix-ui/react-avatar";
import {Flex, Text} from "@radix-ui/themes";

interface ChatMessageProps {
    currentUser: UserGet;
    conversation: ConversationGet;
    message: ConversationMessage;
    userApi: UserApi;
    messageApi: MessageApi;
}

const ChatMessage = (props: ChatMessageProps) => {
    const {
        currentUser,
        conversation,
        message,
        userApi,
        messageApi,
    } = props;

    const getSender = (): { user_id: number, user: UserInReview, profile_picture: any } => {
        if (conversation.customer_id === currentUser.user_id && message.sender_type === "customer" ||
            conversation.service_provider_id === currentUser.user_id && message.sender_type === "service_provider") {
            return {user_id: currentUser.user_id, user: currentUser, profile_picture: null}
        } else {
            return {
                user_id: conversation.customer_id === currentUser.user_id ? conversation.service_provider_id : conversation.customer_id,
                user: conversation.customer_id === currentUser.user_id ? conversation.service_provider : conversation.customer,
                profile_picture: null
            }
        }
    }

    const [image, setImage] =
        useState<{ format: string, object: string } | null>(null);

    useEffect(() => {
        if (message.message_attachment) {
            messageApi.getImageConversationConversationIdMessageMessageIdMediaGet(
                conversation.conversation_id,
                message.message_id, {responseType: 'blob'}).then(response => {
                if (response.status === 200 && message.message_attachment) {
                    const tmpSplitt = message.message_attachment.split(".");
                    const format = tmpSplitt[tmpSplitt.length - 1];

                    setImage({
                        format: format,
                        // @ts-ignore
                        object: URL.createObjectURL(response.data)
                    });
                }
            })
        }
    }, [])

    const [data, setData] =
        useState<{ user_id: number, user: UserInReview, profile_picture: any } | null>(null);

    useEffect(() => {

        const user = getSender()

        userApi.getImageUserIdImageGet(user.user_id, {responseType: 'blob'}).then(response => {
            if (response.status === 200) {
                // @ts-ignore
                setData({...user, profile_picture: URL.createObjectURL(response.data)});
            }
        })
    }, [])


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

    if (!data) {
        return null;
    }

    return (
        <div style={{
            width: "100%",
            display: "flex",
            gap: "10px",
        }}>
            <div className={"profile-picture"}>
                <Avatar.Root className="AvatarRoot-Message">
                    <Avatar.Image
                        className="AvatarImage"
                        src={data.profile_picture}
                        alt="Colm Tuite"
                    />
                    <Avatar.Fallback className="AvatarFallback" delayMs={600}>
                        CT
                    </Avatar.Fallback>
                </Avatar.Root>
            </div>
            <div className={"chat-panel-text-container"}>
                <Flex direction={"column"} width={"100%"}>
                    <div style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "space-between",
                        alignItems: "center"
                    }}>
                        <Text size={"3"} weight={"bold"}>{`${data.user.first_name} ${data.user.last_name}`}</Text>
                    </div>
                    <div style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "space-between",
                        alignItems: "center",
                    }}>
                        <Text size={"1"}
                              color={message.read_at === null && getSender().user_id !== currentUser.user_id ? "white" : "gray"}
                              weight={message.read_at === null && getSender().user_id !== currentUser.user_id ? "bold" : "normal"}
                        >{message.text ?? "System: Ihr Auftrag wurde zugestellt"}</Text>

                        <Text size={"1"}
                              color={message.read_at === null && getSender().user_id !== currentUser.user_id ? "white" : "gray"}
                              weight={message.read_at === null && getSender().user_id !== currentUser.user_id ? "bold" : "normal"}
                        >{formatTime(new Date(conversation.last_message?.created_at as string))}</Text>
                    </div>
                    {image ? ((image.format === "jpg" || image.format === "jpeg" || image.format === "png") ?
                            <div style={{width: "200px", height: "200px"}}
                                 onClick={() => window.open(image.object, "_blank")}>
                                <img style={{width: "200px", height: "200px", objectFit: "contain"}} src={image.object}
                                     alt={message.message_attachment?.substring(64)}/>
                            </div>
                            :
                            <div style={{width: "100px", height: "100px", marginTop: "10px"}}
                                 onClick={() => window.open(image.object, "_blank")}>
                                <img style={{width: "100px", height: "100px", objectFit: "contain" }}
                                     src={"https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/1200px-PDF_file_icon.svg.png"}
                                     alt={message.message_attachment?.substring(64)}/>
                            </div>)
                        : null}
                </Flex>
            </div>
        </div>
    )
}

export default ChatMessage;