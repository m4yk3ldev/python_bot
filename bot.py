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

user = db.User()

# Para registar el usuario
REGISTEREMAIL, PROVINCIA, TELEFONO, IS_PRINTER3D, YES_IS_PRINTER3D, NO_IS_PRINTER3D = range(6)


def start(update, context):
    text = """
    Listado de comando a usar:
    /info - Propocito del bot
    /registrar3d - Homologo de las preguntas de lista de  https://bit.ly/cuba-3dprinters 
    /cancelar - Cancela el proceso de registro 
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
    user.setUsername(update.message.from_user.username)


def info(update, context):
    logger.info(f"El usuario {update.message.from_user.username} consulto la informacion")
    update.message.reply_text("Este bot facilita la gestion de impresionn 3D")


# Empezar el registar
def registar3d(update, context):
    logger.info(f"El usuario {update.message.from_user.username} pide registar")
    update.message.reply_text("Por favor introduzca el correo")
    return REGISTEREMAIL


# Registar los email
def registeremail(update, context):
    email = str(update.message.text)
    update.message.reply_text(f"Registrado el correo {email}")
    user.setCorreo(email)
    update.message.reply_text("Por favor inserte su # de telefono , si no lo deseas /skip para pasar")
    return TELEFONO


def skip_phone(update, context):
    reply_keyboard = [
        ['Pinar del Río',
         'Artemisa',
         'Mayabeque',
         'Matanzas',
         'Cienfuegos',
         'Villa Clara',
         'Sancti Spiritus',
         'Ciego de Ávila',
         'Camagüey',
         'Holguín',
         'Granma',
         'Santiago de Cuba',
         'Guantánamo',
         'Isla de la Juventud',
         'Habana',
         ]
    ]
    update.message.reply_text("Cual es su provincia?", resize_keyboard=True,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return PROVINCIA


# Registar el telefono
def registrarphone(update, context):
    telefono = str(update.message.text)
    user.setTelefono(telefono)

    reply_keyboard = [
        ['Pinar del Río',
         'Artemisa',
         'Mayabeque',
         'Matanzas',
         'Cienfuegos',
         'Villa Clara',
         'Sancti Spiritus',
         'Ciego de Ávila',
         'Camagüey',
         'Holguín',
         'Granma',
         'Santiago de Cuba',
         'Guantánamo',
         'Isla de la Juventud',
         'Habana',
         ]
    ]
    update.message.reply_text("Cual es su provincia?", resize_keyboard=True,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return PROVINCIA


# Registar la provincia
def registarProvincia(update, context):
    provincia = str(update.message.text)
    user.setProvincia(provincia)
    update.message.reply_text(f"Provincia actualizada {provincia}")
    reply_keyboard = [['Si', 'No', ]]
    update.message.reply_text("Tienes impresora?",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return IS_PRINTER3D


# Register si Printer3d
def registar_isPrinter3D(update, context):
    is_printer = (update.message.text == "Si")
    if is_printer:
        return YES_IS_PRINTER3D
    else:
        return NO_IS_PRINTER3D


# Cancelar el registro
def cancel(update, context):
    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text('Cancelada el registro')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(cfg.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('registrar3d', registar3d)],

        states={
            REGISTEREMAIL: [MessageHandler(Filters.text, registeremail)],
            TELEFONO: [MessageHandler(Filters.text, registrarphone),
                       CommandHandler('skip', skip_phone)],
            PROVINCIA: [MessageHandler(Filters.text, registarProvincia)],
            IS_PRINTER3D: [MessageHandler(Filters.regex('^(Si|No)$'), registar_isPrinter3D)],
        },

        fallbacks=[CommandHandler('cancelar', cancel)]

    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("info", info))

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
