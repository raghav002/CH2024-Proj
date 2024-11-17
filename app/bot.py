from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the UW-Madison Course Recommender! Type /recommend to get started.")

async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_interests = " ".join(context.args)
    if not user_interests:
        await update.message.reply_text("Please provide your interests, e.g., /recommend cryptography machine learning.")
        return

    # Replace this with your actual recommendation logic
    recommendations = ["CS540 - Artificial Intelligence", "CS564 - Database Management"]
    response = "Here are some course recommendations for you:\n"
    response += "\n".join(recommendations)

    await update.message.reply_text(response)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Please provide the course code and feedback score, e.g., /feedback CS540 5.")
        return

    course_code, feedback_score = context.args[0], int(context.args[1])
    # Replace this with your feedback-saving logic
    await update.message.reply_text(f"Feedback for {course_code} with score {feedback_score} received. Thank you!")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("recommend", recommend))
    application.add_handler(CommandHandler("feedback", feedback))

    application.run_polling()
