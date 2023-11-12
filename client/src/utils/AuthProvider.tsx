import {ReactNode, useEffect, useMemo, useState} from "react";
import Auth from "./Auth.tsx";
import {Configuration, TokenApi, UserApi, UserGet} from "../api";

interface AuthData {
    tokenApi: TokenApi;
    userApi: UserApi;
    user: string;
    password: string;
}


function AuthProvider(props: { children: ReactNode }) {

    const fetchUser = async (token: string) => {
        const response = await data?.userApi.getCurrentUserUserMeGet({headers: {Authorization: `Bearer ${token}`}});
        if (!response || response.status !== 200) {
            throw new Error("Could not fetch user");
        }
        return response.data;
    }

    const getTokenFromCookie = async () => {
        const token = readFromCookie("token");
        if (token === null) {
            throw new Error("No token found");
        }
        return token;
    }

    const [data, setData] = useState<AuthData>(
        {
            tokenApi: new TokenApi(new Configuration({basePath: "api"})),
            userApi: new UserApi(new Configuration({basePath: "api"})),
            user: "",
            password: ""
        }
    );
    const [loading, setLoading] = useState<boolean>(true);

    const [currentUser, setCurrentUser] = useState<UserGet | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

    useEffect(() => {
        async function init() {
            try {
                const token = await getTokenFromCookie();
                const user = await fetchUser(token);
                setToken(token);
                setCurrentUser(user);
                setIsAuthenticated(true);
            } catch (e) {
            }
            setLoading(false);
        }

        init();
    }, [])

    const readFromCookie = (name: string) => {
        const nameEQ = name + "=";
        const ca = document.cookie.split(";");
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === " ") c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0)
                return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    const valueWrapper = useMemo(
        () => ({
            data,
            setData,
            currentUser,
            setCurrentUser,
            loading,
            setLoading,
            token,
            setToken,
            isAuthenticated,
            setIsAuthenticated
        }), [data, currentUser, loading, token, isAuthenticated]
    );

    return <Auth.Provider value={valueWrapper}>{props.children}</Auth.Provider>;
}

export default AuthProvider;