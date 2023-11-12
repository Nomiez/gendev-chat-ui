import useAuth from "../hooks/UseAuth.tsx";
import {VNode} from "preact";
import {useEffect} from "preact/compat";
import {useNavigate} from "react-router-dom";
import * as Progress from '@radix-ui/react-progress';
import {useState} from "react";
import "./styleSecureComponent.css"

function SecureComponent(props: { children: VNode, loginPath: string }) {
    const {loading, isAuthenticated} = useAuth();
    const navigate = useNavigate();

    const [progress, setProgress] = useState(0);

    useEffect(() => {
        const timer = setTimeout(() => setProgress(100), 500);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        if (loading) {
            return;
        }
        if (!isAuthenticated) {
            navigate(props.loginPath);
        }
        console.log(isAuthenticated)
    }, [isAuthenticated, loading]);


    if (loading) {
        return (
            <div style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                alignContent: "center",
                width: "100vw",
                height: "100vh",
            }}>
                <Progress.Root className="ProgressRoot" value={progress}>
                    <Progress.Indicator
                        className="ProgressIndicator"
                        style={{transform: `translateX(-${100 - progress}%)`}}
                    />
                </Progress.Root>
            </div>
        );
    } else {
        return props.children;
    }

}

export default SecureComponent;