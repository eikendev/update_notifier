import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters

from . import commands


def error(update: Update, context: CallbackContext):
    if update is not None:
        logging.warn('Update %s caused error %s.', update, error)


def add_handlers(dp):
    dp.add_error_handler(error)

    handlers = [
        CommandHandler('start', commands.command_start),
        CommandHandler('help', commands.command_help),
        CommandHandler('ping', commands.command_ping),
        CommandHandler('subscribe', commands.command_subscribe),
        CommandHandler('unsubscribe', commands.command_unsubscribe),
        CommandHandler('status', commands.command_status),
        CommandHandler('peek', commands.command_peek),
        # For unknown commands we add a low-priority handler.
        MessageHandler(Filters.command, commands.command_unknown)
    ]

    for handler in handlers:
        dp.add_handler(handler)
