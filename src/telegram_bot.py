import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv


# importar as variáveis de ambiente
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# armazenamento de resposta do usuário
user_response = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, sou o seu Assistente Médico AI, uma inteligência artificial projetada para ajudar você a entender melhor sua saúde. Meu objetivo é fornecer informações claras e confiáveis para ajudá-lo(a) a tomar decisões informadas sobre o seu bem-estar, tudo com segurança e privacidade. Estou em desenvolvimento e embora ainda não possamos conversar sobre seus sintomas, Posso interpretar seus exames médicos e dar orientações sobre seu estado de saúde.")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="[ Iniciando atendimento ]")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envie o exame que você quer que eu analise para você no formato PDF ou DOCX:")


async def file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Desculpe, mas este arquivo não é um PDF ou DOCX. Preciso que envie um resultado de exame PDF ou DOCX.")
        return

    new_file = await update.message.effective_attachment.get_file()





async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="No momento estamos recebendo somente arquivos PDF ou DOCX de exames. Em breve daremos suporte à funcionalidade de chat.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("bot_father_token")).build()


    start_handler = CommandHandler('start', start)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), text)
    file_handler = MessageHandler(filters.ATTACHMENT, file)

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(file_handler)

    application.run_polling()