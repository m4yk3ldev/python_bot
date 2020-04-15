import logging

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import cfg
import db

# Enable logging
logging.basicConfig(
    format=' ######### %(asctime)s - %(name)s - %(levelname)s - %(message)s #########',
    level=logging.INFO)

logger = logging.getLogger(__name__)

user = db.User()

provincias = [
    ['Pinar del Río',
     'Artemisa'],
    ['Mayabeque',
     'Matanzas'],
    ['Cienfuegos',
     'Villa Clara'],
    ['Sancti Spiritus',
     'Ciego de Ávila'],
    ['Camagüey',
     'Las Tunas'],
    ['Holguín',
     'Granma'],
    ['Santiago de Cuba',
     'Guantánamo'],
    ['Isla de la Juventud',
     'Habana'],
]
# Para registar el usuario
REGISTEREMAIL, PROVINCIA, TELEFONO, IS_PRINTER3D, YES_IS_PRINTER3D, NO_IS_PRINTER3D, CANT_FDM, DIAMETROFILAMENTO, CANT_SLA_DLP, IS_CNC, CNC, RESERVA, MATERIAL_CNC = range(
    13)


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
    if user.username is None:
        user.setUsername(update.message.from_user.username)
    logger.info(f" {user.username} a iniciado el bot")


def info(update, context):
    logger.info(
        f"El usuario {update.message.from_user.username} consulto la informacion")
    if user.username is None:
        user.setUsername(update.message.from_user.username)
    update.message.reply_text("Este bot facilita la gestion de impresionn 3D")


# Empezar el registar
def registar3d(update, context):
    if user.username is None:
        user.setUsername(update.message.from_user.username)
    logger.info(f"El usuario {user.username} pide registar")
    update.message.reply_text("Por favor introduzca el correo")
    return REGISTEREMAIL


# Registar los email
def registeremail(update, context):
    logger.info(f" {user.username}  accedio a registeremail")
    email = str(update.message.text)
    update.message.reply_text(f"Registrado el correo {email}")
    user.setCorreo(email)
    update.message.reply_text(
        "Por favor inserte su # de telefono , si no lo deseas /skip para pasar")
    return TELEFONO


def skip_phone(update, context):
    logger.info(f" {user.username}  accedio a skip_phone")
    update.message.reply_text(
        "Cual es su provincia?",
        resize_keyboard=True,
        reply_markup=ReplyKeyboardMarkup(provincias),
        one_time_keyboard=True)
    return PROVINCIA


# Registar el telefono
def registrarphone(update, context):
    logger.info(f" {user.username}  accedio a registerphone")
    telefono = str(update.message.text)
    logger.info(f"{telefono}")
    if telefono == "/skip":
        update.message.reply_text("Bueno despues puede poner el # si desea")
    else:
        update.message.reply_text('Gracias')
        user.setTelefono(telefono)

    update.message.reply_text(
        "Cuál es su provincia?",
        resize_keyboard=True,
        reply_markup=ReplyKeyboardMarkup(provincias),
        one_time_keyboard=True)
    return PROVINCIA


# Registar la provincia
def registarProvincia(update, context):
    logger.info(f" {user.username}  accedio a registerProvincia")
    provincia = str(update.message.text)
    user.setProvincia(provincia)
    update.message.reply_text(f"Provincia actualizada {provincia}")
    reply_keyboard = [['Si', 'No', ]]
    update.message.reply_text(
        "Tienes impresora?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard),
        one_time_keyboard=True)
    return IS_PRINTER3D


# Register si Printer3d
def registar_isPrinter3D(update, context):
    logger.info(f" {user.username}  accedio a registar_isPrinter3D")
    is_printer = (update.message.text == "Si")
    if is_printer:
        user.setIs3D()
        update.message.reply_text(
            "El objetivo es determinar la capacidad fuerza de trabajo en maquinaria total disponible"
            " que puede ser destinada a estos fines. \n\n"
            "¿De cuántas impresoras FDM dispone? ")
        return CANT_FDM
    else:
        update.message.reply_text("Tienes herramientas CNC?")
        return IS_CNC


def register_isCNC(update, context):
    logger.info(f" {user.username}  accedio a register_isCNC")
    is_cnc = (update.message.text == "Si")
    user.setIsCNC()
    if is_cnc is True:
        update.message.reply_text(
            "El objetivo es determinar la capacidad fuerza de trabajo en maquinaria total disponible que puede ser "
            "destinada a estos fines./n "
            "¿De cuántas máquinas CNC dispone?")
        return CNC
    else:
        return RESERVA


def register_CNC(update, context):
    logger.info(f" {user.username}  accedio a register_CNC")
    try:
        cant = int(update.message.text)
        user.setCantCNC(cant)
        update.message.reply_text(
            "¿Con qué materiales puede trabajar su máquina herramienta CNC?")
        return MATERIAL_CNC
    except ValueError:
        update.message.reply_text("Debe de introducir un numero")


def registerMaterialCNC(update, context):
    logger.info(f" {user.username}  accedio a register_CNC")
    material = str(update.message.text)
    user.setMaterialesCNC(material)
    db.AddUser(user)
    db.Salvar()
    return RESERVA


# FDM disponible
def register_FDM(update, context):
    logger.info(f" {user.username}  accedio a registar_FDM")
    try:
        cant_fdm = int(update.message.text)
        user.setCantFDM(cant_fdm)
        update.message.reply_text(
            "¿Qué diámetros de filamento plástico puede utilizar su impresora? \n"
            " Ejemplo : 1.75 mm, 2.85mm")
        return DIAMETROFILAMENTO
    except ValueError:
        update.message.reply_text("Debe de introducir un número")


def registarDiametroFilamento(update, context):
    logger.info(f" {user.username}  accedio a registarDiametroFilamento")
    dia_fila = str(update.message.text)
    user.setDiametroFilamento(dia_fila)
    update.message.reply_text("¿De cuántas impresoras SLA o DLP dispone?")
    return CANT_SLA_DLP


def registarCant_SLA_DLP(update, context):
    logger.info(f" {user.username}  accedio a registarCant_SLA_DLP")
    try:
        cant_SLA_DLP = int(update.message.text)
        user.setCantSLA_DLP(cant_SLA_DLP)
        update.message.reply_text("Tiene herramientas CNC?")
        return IS_CNC
    except ValueError:
        update.message.reply_text("Debe de introducir un numero")


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
            CANT_FDM: [MessageHandler(Filters.text, register_FDM)],
            DIAMETROFILAMENTO: [MessageHandler(Filters.text, registarDiametroFilamento)],
            CANT_SLA_DLP: [MessageHandler(Filters.text, registarCant_SLA_DLP)],
            IS_CNC: [MessageHandler(Filters.regex('^(Si|No)$'), register_isCNC)],
            CNC: [MessageHandler(Filters.text, register_CNC)],
            MATERIAL_CNC: [MessageHandler(Filters.text, registerMaterialCNC)],
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
