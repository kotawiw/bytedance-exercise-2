import React from "react";
import {Container, Jumbotron} from "react-bootstrap";
import {useAuthStatus} from "../api";
import {Link} from "react-router-dom";


export const HomePage = () => {
    const { data: authStatus } = useAuthStatus()
    const loggedInEmail = authStatus && authStatus.email;

    return <Container>
        <Jumbotron>
            Welcome,
            { loggedInEmail ?
                <p>You are currently logged in as <b>{loggedInEmail}</b></p>:
                <p>First, please <Link to="/login">login or register</Link></p>
            }

            <ul>
                <li>Go to <Link to="/events">Events</Link> tab to see available events, or create a new one</li>
                <li>Click on an event to see the event details and register for the event</li>
            </ul>

        </Jumbotron>
    </Container>
}