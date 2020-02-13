from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base


class Receiver(Base):
    __tablename__ = 'receivers'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    first_seen = Column(DateTime, nullable=False)
    datetime_subscribed = Column(DateTime)
    times_subscribed = Column(Integer, nullable=False)
    last_messaged = Column(DateTime)
    times_messaged = Column(Integer, nullable=False)

    def __init__(self, chat_id, subscribed=False):
        now = datetime.now()

        self.chat_id = chat_id
        self.first_seen = now
        self.datetime_subscribed = None
        self.times_subscribed = 0
        self.last_messaged = None
        self.times_messaged = 0

        if subscribed:
            self.set_subscribed(timestamp=now)

    def __str__(self):
        return '<Receiver with chat id {}>'.format(self.chat_id)

    @hybrid_property
    def is_subscribed(self):
        return self.datetime_subscribed is not None

    @is_subscribed.expression
    def is_subscribed(cls):
        return cls.datetime_subscribed.isnot(None)

    def set_subscribed(self, timestamp=None):
        if not timestamp:
            timestamp = datetime.now()
        elif type(timestamp) is not datetime:
            raise TypeError('Timestamp must be of type timestamp.timestamp.')

        self.datetime_subscribed = timestamp
        self.times_subscribed += 1

    def set_unsubscribed(self):
        self.datetime_subscribed = None

    def set_messaged(self, timestamp=None):
        """
        :param timestamp: New ``last_messaged`` timestamp for this receiver.
        If omitted, ``last_messaged`` remains unchanged.
        """
        if timestamp is not None:
            if type(timestamp) is datetime:
                self.last_messaged = timestamp
            else:
                raise TypeError('Timestamp must be of type datetime.datetime.')

        self.times_messaged += 1
