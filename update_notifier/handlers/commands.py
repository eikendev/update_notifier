from sqlalchemy.orm.exc import NoResultFound
from telegram import Update
from telegram.ext import CallbackContext

from ..checker import get_versions
from ..database.models import Receiver
from ..decorators import session_request


def command_unknown(update: Update, context: CallbackContext):
    update.message.reply_text('Unknown command.')


@session_request
def command_start(update: Update, context: CallbackContext, session):
    chat_id = update.message.chat_id

    update.message.reply_text('Hello there.')

    try:
        Receiver.query.filter_by(chat_id=chat_id).one()
    except NoResultFound:
        receiver = Receiver(chat_id)
        session.add(receiver)
        session.commit()


def command_help(update: Update, context: CallbackContext):
    update.message.reply_text("I'm here to help.")


def command_ping(update: Update, context: CallbackContext):
    update.message.reply_text('Pong!')


@session_request
def command_subscribe(update: Update, context: CallbackContext, session):
    chat_id = update.message.chat_id

    try:
        receiver = Receiver.query.filter_by(chat_id=chat_id).one()
        if receiver.is_subscribed:
            update.message.reply_text('You already subscribed.')
            return
        else:
            receiver.set_subscribed()
    except NoResultFound:
        receiver = Receiver(chat_id, subscribed=True)
        session.add(receiver)

    session.commit()
    update.message.reply_text('You successfully subscribed.')


@session_request
def command_unsubscribe(update: Update, context: CallbackContext, session):
    chat_id = update.message.chat_id

    try:
        receiver = Receiver.query.filter_by(chat_id=chat_id,
                                            is_subscribed=True).one()

        receiver.set_unsubscribed()
        session.commit()

        update.message.reply_text('You successfully unsubscribed.')
    except NoResultFound:
        update.message.reply_text('You are currently not subscribed.')


@session_request
def command_status(update: Update, context: CallbackContext, session):
    chat_id = update.message.chat_id

    try:
        receiver = Receiver.query.filter_by(chat_id=chat_id).one()

        if receiver.is_subscribed:
            message = 'You are currently subscribed.'
        else:
            message = 'You are currently not subscribed.'

        message += "\nYou were notified {} times.".format(
            receiver.times_messaged)

        if receiver.last_messaged is not None:
            ts = receiver.last_messaged.strftime('%Y-%m-%d %H:%M')
            message += "\nThe last notification was sent on {}.".format(ts)

        update.message.reply_text(message)
    except NoResultFound:
        update.message.reply_text("I don't know you.")


def command_peek(update: Update, context: CallbackContext):
    versions = get_versions()

    if versions is None:
        pass
    else:
        message = "\n".join([e + ': ' + versions[e] for e in versions])
        update.message.reply_text(message)
