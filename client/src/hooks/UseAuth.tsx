import {useContext, useEffect} from "preact/compat";
import Auth from "../utils/Auth.tsx";
import {Configuration, TokenApi, UserApi} from "../api";
import {useNavigate} from "react-router-dom";

function useAuth(loginRedirectUrl: string | null = null,
                 logoutRedirectUrl: string | null = null) {

    const {
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
    } = useContext(Auth);

    const navigate = useNavigate();

    useEffect(() => {
        async function fetchUser() {
            if (token && token !== "") {
                const response = await data?.userApi.getCurrentUserUserMeGet({headers: {Authorization: `Bearer ${token}`}});
                if (!response || response.status !== 200) {
                    setIsAuthenticated(false)
                    return;
                }
                setCurrentUser(response.data);
            }
        }

        fetchUser();
    }, [])

    const login = async (username: string, password: string) => {
        setLoading(true);

        if (data === null) {
            console.error("No auth data provided");
        }

        setData(({
            tokenApi: data?.tokenApi ?? new TokenApi(),
            userApi: data?.userApi ?? new UserApi(),
            user: username,
            password: password
        }));

        const response = await data?.tokenApi.loginTokenPost(username, password);

        if (!response || response.status !== 200) {
            console.error("Login failed");
            return;
        }

        setToken(response.data.access_token);
        setLoading(false);
        setIsAuthenticated(true);
        storeInCookie("token", response.data.access_token, 1)
        if (loginRedirectUrl !== null)
            navigate(loginRedirectUrl);
    }
    const getTokenSilently = async (): Promise<string | null> => {
        if (!isAuthenticated) {
            console.error("Not logged in");
            return null;
        }
        //Check if token is still valid
        const response = await data?.userApi.getCurrentUserUserMeGet({headers: {Authorization: `Bearer ${token}`}});
        if (!response || response.status === 403) {
            const response = await data?.tokenApi.loginTokenPost(data?.user, data?.password);

            if (!response || response.status !== 200 || !response.data.access_token) {
                console.error("Reauthentication failed");
                setIsAuthenticated(false);
                return null;
            }

            setToken(response.data.access_token);
            return response.data.access_token;
        }
        return token;
    }

    const logout = async () => {
        setData(({
            tokenApi: data?.tokenApi ?? new TokenApi(new Configuration({basePath: "api"})),
            userApi: data?.userApi ?? new UserApi(new Configuration({basePath: "api"})),
            user: "",
            password: ""
        }));
        setToken("");
        setCurrentUser(null);
        setIsAuthenticated(false);
        if (logoutRedirectUrl !== null)
            navigate(logoutRedirectUrl);
    }

    const storeInCookie = (name: string, value: string, days: number) => {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = `${name}=${(value || "")}${expires}; path=/; secure`;
    }

    return {
        token,
        currentUser,
        login,
        logout,
        getTokenSilently,
        loading,
        isAuthenticated
    }

}


export default useAuth;