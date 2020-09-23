# Event Webapp

* This webapp allow you to browse available events
* Create an event (require user login/registration)
* Register to an event (require user login/registration)

Note:
* I apologize for miss-reading the assignment. This webapp **does not include** the feature to 
"send a notification email when a person signing up for an event". In fact, it currently cannot send any email. 
Please feel free to give the penalty as appropriate.

# Build and Install

The easiest way to run the service is by [Docker](https://docs.docker.com/).


```bash
docker-compose up
```

This should start the service in http://localhost:5000/

Note that:
- The webapp's database is pre-populated and included in `./instance`
- The webapp's frontend is pre-bundled and included in `./frontend/build`

### Backend (API Server) Development

The backend server is a modified version of [Flask Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/).

You need Python 3. Using a `venv` or `conda` is also recommended. 

```bash
pip install -r requirements.txt
```

To run tests:
```bash
pytest test
```

To start the server:
```bash
export FLASK_APP=server
flask run
```

The default port for the backend http://127.0.0.1:5000/

### Frontend Development

The `./frontend` directory is created by [create-react-app](https://create-react-app.dev/). 

To build the frontend, you will need:
- nodejs (tested on v13.8.0)
- npm (tested on v6.14.6) or yarn (tested on v1.22.0)

```bash
npm install
```

To run the frontend in the development mode on http://localhost:3000, run:
```bash
npm start
```

To build frontend Typescript into a static minified bundle, run:
```bash
npm run build
```

# API References

### Authentication APIs

The authentication is based-on browser session.

#### Authentication Status - GET `/api/auth/status`

Example Response (if logged-in):
```javascript
{
    "email": "user1@gmail.com",
    "loggedIn": true
}
```

Example Response (if NOT logged-in):
```javascript
{
    "loggedIn": false
}
```

#### Login - POST `/api/auth/login`

Example Request:
```javascript
const body = {
    email: "user1@gmail.com",  
    password: "test"   
}

fetch('/api/auth/login', {
    method: 'POST', body: JSON.stringify(body),
}).then(res => res.json())
```
Example Response:
```javascript
{
    "email": "user1@gmail.com",
    "loggedIn": true
}
```

#### Logout - POST, PUT `/api/auth/logout`

* Do not require POST or PUT body
* Return the authentication status before logout

Example Response:
```javascript
{
    "email": "user1@gmail.com",
    "loggedIn": true
}
```

#### Register User - POST `/api/auth/register`

* Have a optional query parameter `autologin` (default `=true`) to automatically log in after the registration.
* Return the authentication status after the registration

Example Request:
```javascript
const body = {
    email: "user1@gmail.com",  
    password: "test"   
}

fetch('/api/auth/register', {
    method: 'POST', body: JSON.stringify(body),
}).then(res => res.json())
```
Example Response:
```javascript
{
    "email": "user1@gmail.com",
    "loggedIn": true
}
```

### Event APIs

#### List Events - GET `/api/events`

Example Response:
```javascript
{
    "totalCount": 3,
    "values":[
        {
            "id": "09abe9db",
            "name": "Xyz",
            "location": "Somewhere",
            "description": "Do in laughter...",
            "endTimestamp": 1600498729000,
            "startTimestamp": 1600412329000
        }, ...
    ]
}
```

#### Get Event - GET `/api/event/<event_id>`

Example Response:
```javascript
{
    "id": "09abe9db",
    "name": "Xyz",
    "location": "Somewhere",
    "description": "Do in laughter...",
    "endTimestamp": 1600498729000,
    "startTimestamp": 1600412329000
}
```

#### Create Event - POST `/api/events`

Example Request:
```javascript
const body = {
    name: "A Party",               // Event's name
    location: "Tokyo",             // Event's location
    description: "Welcome, ...",   // Event's description (optional)
    startTimestamp: 1600417986772, // Milisecond epoach timestamp
    endTimestamp: 1600417996772    // Milisecond epoach timestamp
}

fetch('/api/events', {
    method: 'POST', body: JSON.stringify(body),
}).then(res => res.json())
```

Example Response:
```javascript
{
    "id": "09abe9db",
    "name": "A Party",
    "location": "Tokyo",
    "description": "Welcome, ...",
    "endTimestamp": 1600417986772,
    "startTimestamp": 1600417996772
}
```

### Registration APIs

#### Get Registrations - GET `/api/event/<event_id>/registrations`

Example Response:
```javascript
[
    {"email": "user1@gmail.com"},
    ...
]
```

#### Register - PUT `/api/event/<event_id>/registrations`

* **Required logged-in session**
* Do not require PUT body

Example Response:
```javascript
{
    "email": "user1@gmail.com"
}
```

#### Unregister - PUT `/api/event/<event_id>/registrations`

* **Required logged-in session**
* Do not require PUT body
* Return the registration details if exist

Example Response:
```javascript
{
    "email": "user1@gmail.com"
}
```