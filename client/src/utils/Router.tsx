import {BrowserRouter, Routes, Route} from 'react-router-dom'
import ContextWrapper from './ContextWrapper';
import AuthProvider from "./AuthProvider.tsx";
import {LoginPage} from "../pages/LoginPage.tsx";
import SecureComponent from "./SecureComponent.tsx";
import ChatPage from "../pages/ChatPage.tsx";

/**
 * Returns the pathname of the current Base URL
 * @return {string} The pathname
 */
const getPathname = () => {
    const parser = document.createElement('a');
    parser.href = import.meta.env.BASE_URL;
    return parser.pathname;
};

/**
 * Implementations of the Router.
 * @return {JSX.Element} The Router
 */
function Routing() {
    const LOGIN_PATH = "/login";
    return (
        <BrowserRouter basename={getPathname()}>
            <AuthProvider>
                <Routes>
                    <Route path={LOGIN_PATH} element={<LoginPage/>}/>
                    <Route path="/*" element={
                        <ContextWrapper>
                            <SecureComponent loginPath={LOGIN_PATH}>
                                <Routes>
                                    <Route path="/" element={<ChatPage/>}/>
                                </Routes>
                            </SecureComponent>
                        </ContextWrapper>
                    }/>
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}

export default Routing;
