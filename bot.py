import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
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
REGISTEREMAIL, PROVINCIA, TELEFONO, IS_PRINTER3D, YES_IS_PRINTER3D, NO_IS_PRINTER3D, CANT_FDM, DIAMETROFILAMENTO, \
CANT_SLA_DLP, IS_CNC, CNC, RESERVA, MATERIAL_CNC, CANTPETG = range(14)


def start(update, context):
    text = """
    Listado de comando a usar:
    /info - Propocito del bot
    /registrar3d - Homologo de las preguntas de lista de  https://bit.ly/cuba-3dprinters
    /cancel - Cancela el proceso de registro
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
        user.setID(update.message.from_user.id)
        if not db.isExist(user):
            db.AddUser(user)
            db.Salvar()
        else:
            db.Eliminar(user)
            db.Salvar()
            print(f"Eliminar {user.username}")

        db.AddUser(user)
        db.Salvar()

    logger.info(f" {user.username} a iniciado el bot")


def info(update, context):
    logger.info(
        f"El usuario {update.message.from_user.username} consulto la informacion")
    if user.username is None:
        user.setUsername(update.message.from_user.username)
        user.setID(update.message.from_user.id)
        db.Salvar()
    update.message.reply_text("Este bot facilita la gestion de impresionn 3D", reply_markup=ReplyKeyboardRemove())


# Empezar el registar
def registar3d(update, context):
    if user.username is None:
        user.setUsername(update.message.from_user.username)
    logger.info(f"El usuario {user.username} pide registar")
    update.message.reply_text("Por favor introduzca el correo",
                              reply_markup=ReplyKeyboardRemove())
    return REGISTEREMAIL


# Registar los email
def registeremail(update, context):
    logger.info(f" {user.username}  accedio a registeremail")
    email = str(update.message.text)
    user.setCorreo(email)
    db.Salvar()
    update.message.reply_text(
        "Por favor inserte su # de telefono , si no lo deseas /skip para pasar", reply_markup=ReplyKeyboardRemove())
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
    if telefono == "/skip":
        update.message.reply_text("Bueno despues puede poner el # si desea")
    else:
        update.message.reply_text('Gracias')
        user.setTelefono(telefono)
        db.Salvar()

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
    db.Salvar()
    update.message.reply_text(f"Provincia actualizada {provincia}", reply_markup=ReplyKeyboardRemove())
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
        db.Salvar()
        update.message.reply_text(
            "El objetivo es determinar la capacidad fuerza de trabajo en maquinaria total disponible"
            " que puede ser destinada a estos fines. \n\n"
            "¿De cuántas impresoras FDM dispone? ", reply_markup=ReplyKeyboardRemove())
        return CANT_FDM
    else:
        reply_keyboard = [['Si', 'No', ]]
        update.message.reply_text("Tienes herramientas CNC?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard),
                                  one_time_keyboard=True
                                  )
        return IS_CNC


def register_isCNC(update, context):
    logger.info(f" {user.username}  accedio a register_isCNC")
    is_cnc = (update.message.text == "Si")
    if is_cnc is True:
        user.setIsCNC()
        db.Salvar()
        update.message.reply_text(
            "El objetivo es determinar la capacidad fuerza de trabajo en maquinaria total disponible que puede ser "
            "destinada a estos fines./n "
            "¿De cuántas máquinas CNC dispone?", reply_markup=ReplyKeyboardRemove())
        return CNC
    else:
        return RESERVA


def register_CNC(update, context):
    logger.info(f" {user.username}  accedio a register_CNC")
    try:
        cant = int(update.message.text)
        user.setCantCNC(cant)
        db.Salvar()
        update.message.reply_text(
            "¿Con qué materiales puede trabajar su máquina herramienta CNC? "
            "Ejemplo: Acrílico, Madera, PVC ")
        return MATERIAL_CNC
    except ValueError:
        update.message.reply_text("Debe de introducir un numero")


def registerMaterialCNC(update, context):
    logger.info(f" {user.username}  accedio a register_CNC")
    material = str(update.message.text)
    user.setMaterialesCNC(material)
    db.Salvar()
    update.message.reply_text(
        "Reservas de material para tomar decisiones y priorizar objetivos de impresión."
        "\n Si deseas insertar los datos despues solo escriba /cancel\n"
        "¿De cuántos kg de filamento PLA para impresión dispone?", reply_markup=ReplyKeyboardRemove()
    )
    return RESERVA


# FDM disponible
def register_FDM(update, context):
    logger.info(f" {user.username}  accedio a registar_FDM")
    try:
        cant_fdm = int(update.message.text)
        user.setCantFDM(cant_fdm)
        db.Salvar()
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
    db.Salvar()
    update.message.reply_text("¿De cuántas impresoras SLA o DLP dispone?")
    return CANT_SLA_DLP


def registarCant_SLA_DLP(update, context):
    logger.info(f" {user.username}  accedio a registarCant_SLA_DLP")
    try:
        cant_SLA_DLP = int(update.message.text)
        user.setCantSLA_DLP(cant_SLA_DLP)
        db.Salvar()
        reply_keyboard = [['Si', 'No', ]]
        update.message.reply_text("Tienes herramientas CNC?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard),
                                  one_time_keyboard=True
                                  )
        return IS_CNC
    except ValueError:
        update.message.reply_text("Debe de introducir un numero")


def registarMateriles(update, context):
    logger.info(f" {user.username}  accedio a registarMateriles")
    cant_kg_PLA = int(update.message.text)
    try:
        user.setCantPLA(cant_kg_PLA)
        db.Salvar()
        update.message.reply_text("¿De cuántos kg de filamento PETG para impresión dispone?",
                                  reply_markup=ReplyKeyboardRemove())
    except ValueError:
        update.message.reply_text("Inserte un número")

    return CANTPETG


def registarCantPETG(update, context):
    logger.info(f" {user.username}  accedio a registarCantPETG")
    petg = int(update.message.text)
    try:
        user.setCantPETG(petg)
        db.Salvar()
        update.message.reply_text("¿De cuántos kg de filamento ABS para impresión dispone?")
    except ValueError:
        update.message.reply_text("Inserte un numero")


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
            RESERVA: [MessageHandler(Filters.text, registarMateriles)],
            CANTPETG: [MessageHandler(Filters.text, registarCantPETG)],
        },

        fallbacks=[CommandHandler('cancel', cancel)],

    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("info", info))

    dp.add_error_handler(error)

    updater.start_polling()
    print("I live")

    updater.idle()


if __name__ == '__main__':
    main()
