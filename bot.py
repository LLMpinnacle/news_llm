
from news_file import get_news_from_keyword
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from keys import telegram_key,news_api_key
import logging

import ollama


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.first_name} used /hello command")
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text  # Get user message
    responses=[]
    logger.info(f"User {update.effective_user.first_name} sent a message: {user_message}")

    # Simple response logic
    if user_message.lower() in ["hi", "hello", "hey"]:
        response = "Hello! How can I help you?"
    else:
        data=get_news_from_keyword(user_message.lower())   
        llama_output = ollama.chat(model='llama3.2:latest',messages=[{'role': 'user', 'content': 'mention your opinion only give me positives {}'.format(data)}])
       
        await update.message.reply_text(f"Here is the LLaMA 3.2 output: {llama_output['message']['content']}")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


logger = logging.getLogger(__name__)



if __name__ == "__main__":
    print("🚀 Bot is starting...")  # Simple confirmation
    try:
        app = ApplicationBuilder().token(telegram_key).build()
        app.add_handler(CommandHandler("hello", hello))
        logger.info("✅ Bot is running and listening for commands...")
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        app.run_polling()
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
    finally:
        logger.info("🛑 Bot has stopped")




