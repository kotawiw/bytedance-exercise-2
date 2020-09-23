import React from "react";
import {Button, Col, Container, Form, Row} from "react-bootstrap";
import {createEvent, login, register, useAuthStatus, useEvents, UserStatus} from "../api";
import {useForm} from "react-hook-form";
import styled from "styled-components";

import {parseDate} from "chrono-node";
import {Link} from "react-router-dom";

const EventListContainer = styled.div`
    ul {
        padding: 0;
    }
`;

const EventRow = styled.li`
    list-style: none;
    margin: 10px 0;

    a {
        display: block;
        padding: 10px 10px;
        color:#212529;
        text-style: none;
        text-decoration: none;
        
        :hover {
            background-color: #eee;
        }
    }
    
    p {
        margin: 0;
        font-style: italic;
    }
    
    label {
        margin: 0;
        display: inline-block;
        width: 70px;
        font-style: normal;
    }
`;

const CreateEventFormContainer = styled.div`
  border: solid 1px #ccc;
  padding: 1em;
`;

export const EventListPage = () => {
    const form = useForm();
    const {data: events, mutate} = useEvents();
    const {data: authStatus} = useAuthStatus();
    if (!events) {
        return null;
    }

    return <div>
        <Container>
            <Row>
                <Col>
                    <EventListContainer>
                        <h2>Events ({events.totalCount})</h2>
                        <ul>
                            {events.values.map(e => {
                                return <EventRow key={e.id}>
                                    <Link to={ "/event/" + e.id }>
                                        <h3>{e.name}</h3>
                                        <p><label>Start:</label> {new Date(e.startTimestamp).toISOString()}</p>
                                        <p><label>End:</label> {new Date(e.endTimestamp).toISOString()}</p>
                                        <p><label>Location:</label> {e.location}</p>
                                    </Link>
                                </EventRow>
                            })}
                        </ul>

                    </EventListContainer>
                </Col>

                <Col xs={4}>
                    <CreateEventFormContainer>
                        {EventCreationForm(form, authStatus, () => mutate())}
                    </CreateEventFormContainer>
                </Col>
            </Row>
        </Container>
    </div>
}

function EventCreationForm(
    form: any,
    authStatus: UserStatus | undefined,
    submitCallback: () => {},
) {
    if (!authStatus || !authStatus.loggedIn) {
        return <p>Please log in to create an event.</p>
    }

    const onSubmit = (data: any) => {
        const {name, location, description, startDatetime, endDatetime} = data;

        const parsedStartDatetime = parseDate(startDatetime);
        if (!parsedStartDatetime) {
            return alert("Invalid input start date");
        }

        const parsedEndDatetime = parseDate(endDatetime);
        if (!parsedEndDatetime) {
            return alert("Invalid input end date");
        }

        const startTimestamp = parsedStartDatetime.getTime();
        const endTimestamp = parsedEndDatetime.getTime();
        return createEvent({name, description, location, startTimestamp, endTimestamp}).then(res => {
            if ('message' in res) {
                return alert(res.message)
            }

            form.reset()
            submitCallback();
        });
    }

    return <div>
        <h3>Create Event</h3>
        <Form onSubmit={form.handleSubmit(onSubmit)}>
            <Form.Group>
                <Form.Label>Name</Form.Label>
                <Form.Control ref={form.register} name="name" type="text"/>
            </Form.Group>

            <Form.Group>
                <Form.Label>Location</Form.Label>
                <Form.Control ref={form.register} name="location" type="text"/>
            </Form.Group>

            <Form.Group>
                <Form.Label>Description</Form.Label>
                <Form.Control ref={form.register} name="description" type="textarea"/>
            </Form.Group>

            <Form.Group>
                <Form.Label>Start Date/Time</Form.Label>
                <Form.Control ref={form.register} name="startDatetime" type="text"
                              placeholder="e.g. Today, Tomorrow, next Friday" />
            </Form.Group>

            <Form.Group>
                <Form.Label>End Date/Time</Form.Label>
                <Form.Control ref={form.register} name="endDatetime" type="text"
                              placeholder="e.g. Today, Tomorrow, next Friday" />
            </Form.Group>

            <Button variant="primary" type="submit">
                Create
            </Button>
        </Form>
    </div>
}

