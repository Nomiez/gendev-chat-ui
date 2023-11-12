import useAuth from "../hooks/UseAuth.tsx";
import * as Form from '@radix-ui/react-form';
import {useRef} from "preact/compat";
import './styleLoginPage.css';

export const LoginPage = () => {
    const {login} = useAuth("/", "/login")

    const email = useRef<HTMLInputElement>(null);
    const password = useRef<HTMLInputElement>(null);

    const handleSubmit = async (event: any) => {
        event.preventDefault()
        const em = email.current?.value
        const pw = password.current?.value
        if (!em || !pw)
            console.error("Email or password not set")
        else {
            await login(em, pw)
        }
    }

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            alignContent: "center",
            justifyContent: "center",
            width: "100vw",
            height: "100vh",
        }}>
            <Form.Root className="FormRoot">
                <Form.Field className="FormField" name="email">
                    <div style={{display: 'flex', alignItems: 'baseline', justifyContent: 'space-between'}}>
                        <Form.Label className="FormLabel">Email</Form.Label>
                        <Form.Message className="FormMessage" match="valueMissing">
                            Please enter your email
                        </Form.Message>
                        <Form.Message className="FormMessage" match="typeMismatch">
                            Please provide a valid email
                        </Form.Message>
                    </div>
                    <Form.Control asChild>
                        <input ref={email} className="Input" type="email" required/>
                    </Form.Control>
                </Form.Field>
                <Form.Field className="FormField" name="password">
                    <div style={{display: 'flex', alignItems: 'baseline', justifyContent: 'space-between'}}>
                        <Form.Label className="FormLabel">Password</Form.Label>
                        <Form.Message className="FormMessage" match="valueMissing">
                            Please enter your Password
                        </Form.Message>
                        <Form.Message className="FormMessage" match="typeMismatch">
                            Please provide a valid password
                        </Form.Message>
                    </div>
                    <Form.Control asChild>
                        <input ref={password} className="Input" type="password" required/>
                    </Form.Control>
                </Form.Field>
                <Form.Submit asChild>
                    <button className="Button" style={{marginTop: 10}} onClick={(e) => handleSubmit(e)}>
                        Post question
                    </button>
                </Form.Submit>
            </Form.Root>
        </div>
    );
};