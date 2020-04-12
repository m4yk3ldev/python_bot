#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import cfg
import os
import db
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

REGISTER3D = range(1)


def start(update, context):
    text = """
    Listado de comando a usar:
    /info - Propocito del bot
    /registrar3d - Homologo de las preguntas de lista de  https://bit.ly/cuba-3dprinters 
    /registrar_cnc - Registrar el CNC
    /recibir_pla - Notificar recepcion de filamento PLA
    /recibir_petg - Notificar recepcion de filamento PETG
    /recibir_abs - Notificar recepcion de filamento ABS
    /recibir_pvc - Notificar recepcion de filamento PVC
    /recibir_pantallas  - Notificar recepción de placas transparentes para viseras
    /recibir_acrilico - Notificar recepción de planchas de acrílico
    /reportar_viseras - Notificar cantidad de viseras hechas
    /entregar_viseras - Notificar cantidad de viseras entregadas
    /resumen - Resúmen de las viseras y material entregado
    
    
    """
    update.message.reply_text(text)


def info(update, context):
    logger.info(f"El usuario {update.message.from_user.username} consulto la informacion")
    update.message.reply_text("Este bot facilita la gestion de impresionn 3D")


def registar3d(update, context):
    logger.info(f"El usuario {update.message.from_user.username} pide registar")
    user = update.message.from_user
    us = db.User()
    us.id = user.id
    us.username = user.username
    db.AddUser(us)


# Cancelar el registro
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Cancelada el registro')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(cfg.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTER3D: [MessageHandler(Filters.text, registar3d)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(conv_handler)

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print("I live")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
