import {createContext} from 'preact';
import {
    UserGet, TokenApi, UserApi, Configuration
} from '../api';
import {StateUpdater} from "preact/hooks";

interface AuthData {
    tokenApi: TokenApi;
    userApi: UserApi;
    user: string;
    password: string;
}

/* init context */
const Auth = createContext<{
    data: AuthData;
    setData: StateUpdater<AuthData>;
    currentUser: UserGet | null;
    setCurrentUser: StateUpdater<UserGet | null>;
    loading: boolean;
    setLoading: StateUpdater<boolean>;
    token: string | null;
    setToken: StateUpdater<string | null>;
    isAuthenticated: boolean;
    setIsAuthenticated: StateUpdater<boolean>;
}>({
    data: {
        tokenApi: new TokenApi(new Configuration({basePath: "api"})),
        userApi: new UserApi(new Configuration({basePath: "api"})),
        user: "",
        password: ""
    },
    setData: () => {
    },
    currentUser: null,
    setCurrentUser: () => {
    },
    loading: false,
    setLoading: () => {
    },
    token: null,
    setToken: () => {
    },
    isAuthenticated: false,
    setIsAuthenticated: () => {
    }
});

export default Auth;
