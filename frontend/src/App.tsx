import React from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";

import './App.scss';
import {HomePage} from "./pages/HomePage"
import {LoginPage} from "./pages/LoginPage";
import {EventListPage} from "./pages/EventListPage";
import {Nav, Navbar, Container} from "react-bootstrap";
import styled from "styled-components";
import {EventPage} from "./pages/EventPage";
import {useAuthStatus} from "./api";


const AppContainer = styled.div`
  padding: 4em 0em;
`;

function App() {
    const { data: authStatus } = useAuthStatus()

    return (
        <div className="App">
            <Router>
                <Navbar bg="light" variant="light">
                    <Nav className="mr-auto">
                        <Link className="nav-link" to="/">Home</Link>
                        <Link className="nav-link" to="/events">Events</Link>
                    </Nav>

                    <Nav>
                        <Link className="nav-link" to="/login">{
                            (authStatus && authStatus.loggedIn) ? "Logout" : "Login"
                        }</Link>
                    </Nav>
                </Navbar>

                <AppContainer>
                    <Switch>
                        <Route path="/login">
                            <LoginPage />
                        </Route>
                        <Route path="/event/:id">
                            <EventPage />
                        </Route>
                        <Route path="/events">
                            <EventListPage />
                        </Route>
                        <Route path="/">
                            <HomePage />
                        </Route>
                    </Switch>
                </AppContainer>
            </Router>
        </div>
    );
}

export default App;
