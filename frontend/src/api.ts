import useSWR from "swr"
import {responseInterface} from "swr/dist/types";

// @ts-ignore
const fetcher = (...args) => fetch(...args).then(res => res.json())

export interface Error {
    message: string
}

export interface UserStatus {
    email?: string;
    loggedIn: boolean;
}

export interface Event {
    id?: string;
    name: string;
    location: string;
    description: string;
    startTimestamp: number;
    endTimestamp: number;
}

export interface EventList {
    totalCount: number;
    values: Event[];
}

export interface Registration {
    email: string
}

export function logout() : Promise<UserStatus | Error> {
    console.log("log out")
    return fetch('/api/auth/logout', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(res => res.json())
}

export function login(data: {email: string, password: string}) : Promise<UserStatus | Error> {
    return fetch('/api/auth/login', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(res => res.json())
}

export function register(data: {email: string, password: string}) : Promise<UserStatus | Error> {
    return fetch('/api/auth/register', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(res => res.json())
}


export function createEvent(data: Event) : Promise<Event | Error> {
    return fetch('/api/events', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(res => res.json())
}

export function registerEvent(event_id: string) : Promise<Event | Error> {
    return fetch(`/api/event/${event_id}/registrations`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(res => res.json())
}

export function unregisterEvent(event_id: string) : Promise<Event | Error> {
    return fetch(`/api/event/${event_id}/registrations`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(res => res.json())
}

// Hooks API

export function useEvents() : responseInterface<EventList, any> {
    return useSWR('/api/events', fetcher)
}

export function useEvent(id: string) : responseInterface<Event, any> {
    return useSWR(`/api/event/${id}`, fetcher)
}

export function useEventRegistrations(id: string) : responseInterface<Registration[], any> {
    return useSWR(`/api/event/${id}/registrations`, fetcher)
}

export function useAuthStatus() : responseInterface<UserStatus, any> {
    return useSWR('/api/auth/status', fetcher)
}