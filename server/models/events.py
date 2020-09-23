import time

from sqlalchemy.orm import Query

from . import db
from .users import User
from .identifiers import id_to_identifier, id_from_identifier


def timestamp_ms():
    return int(time.time() * 1000)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('event.id'), index=True)

    name = db.Column(db.String(5000), unique=False, nullable=False)
    location = db.Column(db.String(5000), unique=False, nullable=False)
    description = db.Column(db.String(1_000_000), unique=False, nullable=False)
    start_timestamp = db.Column(db.Integer(), unique=False, nullable=False)
    end_timestamp = db.Column(db.Integer(), unique=False, nullable=False)

    @property
    def identifier(self):
        return id_to_identifier(self.id)

    @staticmethod
    def create(user, map_like_event):
        event = Event(
            name=_check_event_name(map_like_event.get('name')),
            location=_check_event_location(map_like_event.get('location')),
            description=_check_event_decription(map_like_event.get('description')),
            start_timestamp=_check_event_start_timestamp(map_like_event.get('startTimestamp')),
            end_timestamp=_check_event_start_timestamp(map_like_event.get('endTimestamp'))
        )
        event.owner_user_id = user.id
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def query_events(offset=0, limit=10):
        q: Query = Event.query
        q = q.order_by(Event.start_timestamp)
        count = q.count()
        q.offset(offset)
        q.limit(limit)

        return count, q.all()

    @staticmethod
    def by_identifier(identifier):
        event_id = id_from_identifier(identifier)
        return Event.query.get(event_id)

    def __repr__(self):
        return '<Event %r:%r>' % (self.id, self.identifier)


class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    timestamp = db.Column(db.Integer(), unique=False, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('event_id', 'user_id', name='_event_user_uc'),)

    @staticmethod
    def by_event(event: Event) -> list:
        return EventRegistration.query.filter(EventRegistration.event_id == event.id).all()

    @staticmethod
    def by_event_user(event: Event, user: User):
        return EventRegistration.query \
            .filter(EventRegistration.event_id == event.id) \
            .filter(EventRegistration.user_id == user.id) \
            .first()

    @staticmethod
    def register(event: Event, user: User):
        registration = EventRegistration(event_id=event.id, user_id=user.id)
        registration.timestamp = timestamp_ms()
        db.session.add(registration)
        db.session.commit()
        return registration

    @staticmethod
    def unregister(registration):
        db.session.delete(registration)
        db.session.commit()


def _check_event_name(input):
    if not input \
            or type(input) != str \
            or len(input) == 0:
        raise ValueError("Invalid event's name")

    return input


def _check_event_location(input):
    if not input \
            or type(input) != str \
            or len(input) == 0:
        raise ValueError("Invalid event's location")

    return input


def _check_event_end_timestamp(input):
    if not input or type(input) != int:
        raise ValueError("Invalid end timestamp")

    return input


def _check_event_start_timestamp(input):
    if not input or type(input) != int:
        raise ValueError("Invalid start timestamp")

    return input


def _check_event_decription(input):
    if not input:
        input = ''

    if type(input) != str:
        raise ValueError("Invalid event's description")

    return input
