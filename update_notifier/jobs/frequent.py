import logging

from datetime import datetime

from telegram import ParseMode
from telegram.error import TelegramError
from telegram.ext import CallbackContext

from ..checker import get_updates
from ..config import config
from ..database.models import Receiver
from ..decorators import session_request

notification_text = config['GENERAL']['NotificationText']


@session_request
def job_check_updates(context: CallbackContext, session):
    now = datetime.now()

    receivers = Receiver.query.filter_by(is_subscribed=True).all()
    logging.debug('Query returned %d receivers.', len(receivers))

    updates = get_updates()

    for u in updates:
        logging.debug('Sending update notifications for %s.', u.name)
        message = "*{} {}*\n{}\n[Download]({})"
        message = message.format(u.name, u.version, notification_text, u.href)

        for r in receivers:
            try:
                context.bot.send_message(chat_id=r.chat_id,
                                         text=message,
                                         parse_mode=ParseMode.MARKDOWN)
                r.set_messaged(timestamp=now)
            except TelegramError:
                pass

    session.commit()
