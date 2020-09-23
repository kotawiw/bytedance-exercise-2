from flask import Blueprint, request, abort, jsonify
from flask import g

from server.auth import login_required
from server.models.users import User
from server.models.events import Event
from server.models.events import EventRegistration

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/events", methods=("GET",))
def query_events():
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=10, type=int)

    total_count, events = Event.query_events(offset=offset, limit=limit)
    return jsonify(
        totalCount=total_count,
        values=[event_output(e) for e in events])


@bp.route("/events", methods=("POST",))
@login_required
def create_event():
    user = g.user
    event = Event.create(
        user, request.json
    )

    return event_output(event)


@bp.route("/event/<string:event_id>", methods=("GET",))
def get_event(event_id):
    event = Event.by_identifier(event_id)
    if not event:
        return abort(404, 'Event not found')

    return event_output(event)


@bp.route("/event/<string:event_id>/registrations", methods=("GET",))
def get_registrations(event_id):
    event = Event.by_identifier(event_id)
    if not event:
        return abort(404, 'Event not found')

    registrations = EventRegistration.by_event(event)
    return jsonify([registration_output(r) for r in registrations])


@bp.route("/event/<string:event_id>/registrations", methods=("PUT",))
def register_event(event_id):
    event = Event.by_identifier(event_id)
    if not event:
        return abort(404, 'Event not found')

    user = g.user
    if not user:
        return abort(401, 'Please login to register for an event')

    register = EventRegistration.register(event, user)
    return registration_output(register)


@bp.route("/event/<string:event_id>/registrations", methods=("DELETE",))
def unregister_event(event_id):
    user = g.user
    if not user:
        return abort(401, 'Please login to unregister for an event')

    event = Event.by_identifier(event_id)
    if not event:
        return abort(404, 'Event not found')

    register = EventRegistration.by_event_user(event, user)
    if not register:
        return abort(404, 'Event registration not found')

    EventRegistration.unregister(register)
    return registration_output(register)


def event_output(event: Event):
    return dict(
        id=event.identifier,
        name=event.name,
        location=event.location,
        description=event.description,
        startTimestamp=event.start_timestamp,
        endTimestamp=event.end_timestamp)


def registration_output(registration: EventRegistration):
    # Todo: De-normalize registration info to include user email
    user = User.query.get(registration.user_id)

    return dict(
        email=user.email
    )
