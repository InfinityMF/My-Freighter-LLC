import logging
import os
from io import BytesIO

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from PIL import Image
import pytesseract

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if TELEGRAM_TOKEN is None:
    raise RuntimeError("Environment variable TELEGRAM_TOKEN is required")

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    update.message.reply_text(
        "Отправьте изображение с текстом, и бот пришлет распознанный текст в ответ."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process an incoming photo and reply with recognized text."""
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    file_bytes = await photo_file.download_as_bytearray()

    image = Image.open(BytesIO(file_bytes))
    text = pytesseract.image_to_string(image, lang="rus")

    if not text.strip():
        text = "Текст не найден"

    await update.message.reply_text(text)


def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.run_polling()


if __name__ == "__main__":
    main()
