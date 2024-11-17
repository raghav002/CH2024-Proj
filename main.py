from app.database import create_tables
from app.data_ingestion import update_database
from app.bot import run_bot

if __name__ == "__main__":
    # Initialize database
    create_tables()

    # Update course database dynamically
    update_database()

    # Start Telegram bot
    run_bot()