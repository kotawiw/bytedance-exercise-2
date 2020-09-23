
import React from "react";
import {Col, Container, Row, Form, Button} from "react-bootstrap";
import {Link, useParams} from "react-router-dom";
import {registerEvent, unregisterEvent, useAuthStatus, useEvent, useEventRegistrations} from "../api";
import styled from "styled-components";


const EventInfo = styled.p`
    margin: 10px 0;
    label {
        margin: 0;
        margin-right: 5px;
        display: inline-block;
        width: 80px;
        text-align: right;
    }
`;

const EventDescription = styled.p`
    margin: 30px 0;
    
`;


export const EventPage = () => {
    const { id: event_id } = useParams();
    const {data: authStatus} = useAuthStatus();
    const {data: event} = useEvent(event_id);
    const {data: registrations, mutate} = useEventRegistrations(event_id);
    if (!event) {
        return <div>Fail loading event...</div>
    }

    const startDate = new Date(event.startTimestamp);
    const endDate = new Date(event.endTimestamp);

    const loggedIn = authStatus && authStatus.loggedIn;
    const joined = authStatus && registrations &&
        registrations.find(r => r.email == authStatus.email);

    return <Container>
        <Row>
            <Col>
                <h1>{event.name}</h1>
                <EventInfo>
                    <label>Location:</label>{event.location}
                </EventInfo>

                <EventInfo>
                    <label>Start:</label>
                    <span>{startDate.toDateString()}</span>
                    <span>{startDate.toTimeString()}</span>
                </EventInfo>
                <EventInfo>
                    <label>End:</label>
                    <span>{endDate.toDateString()}</span>
                    <span>{endDate.toTimeString()}</span>
                </EventInfo>

                <EventDescription>{event.description}</EventDescription>

                <h4>Attendances ({registrations?.length})</h4>
                <ul>
                    {registrations?.map(reg => {
                        return <li key={reg.email}>{reg.email}</li>
                    })}
                </ul>

                { !loggedIn &&
                <p>Please log in to register.</p>
                }

                { loggedIn && !joined &&
                <Button variant="primary" onClick={() => registerEvent(event_id).then(() => mutate())}>Join</Button>
                }

                { loggedIn && joined &&
                <Button variant="danger" onClick={() => unregisterEvent(event_id).then(() => mutate())}>Cancel Registration</Button>
                }



            </Col>
        </Row>
    </Container>

}