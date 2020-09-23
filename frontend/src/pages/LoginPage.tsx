import React from "react";
import {Button, Form, Container, Row, Col} from "react-bootstrap";
import useSWR from "swr";
import {useForm} from "react-hook-form";
import {register, login, logout, useAuthStatus, UserStatus} from "../api";
import { useHistory } from "react-router-dom";

export const LoginPage = () => {
    const history = useHistory();
    const form = useForm();
    const { data: authStatus, mutate } = useAuthStatus()

    const tryLogin = (data: any) => {
        return login(data).then(res => {
            if ('loggedIn' in res && res.loggedIn) {
                return history.push("/");
            }

            return register(data).then((res) => {
                if ('loggedIn' in res && res.loggedIn) {
                    return history.push("/");
                }

                if ('message' in res) {
                    return alert(res.message)
                }
            })
        });
    }

    const tryLogout = () => {
        return logout().then(res => {
            if ('message' in res) {
                return alert(res.message)
            }

            return history.push("/");
        })
    }



    if (authStatus && authStatus.loggedIn) {
        return <div>
            <Container>
                <Row>
                    <Col>
                        <p>You are currently logged in as <b>{authStatus.email}</b></p>
                        <Form onSubmit={form.handleSubmit(tryLogout)}>
                            <Button variant="danger" type="submit">
                                Logout
                            </Button>
                        </Form>
                    </Col>
                </Row>
            </Container>
        </div>
    }

    return <div>
        <Container>
            <Row>
                <Col>
                    <Form onSubmit={form.handleSubmit(tryLogin)}>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Email</Form.Label>
                            <Form.Control ref={form.register} name="email" type="email" placeholder="Enter email" />
                        </Form.Group>

                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control ref={form.register} name="password" type="password" placeholder="Password" />
                        </Form.Group>
                        <Button variant="primary" type="submit" value="login">
                            Login / Register
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    </div>
}
