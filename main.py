"""
Main entry point for the AI Agent Chatbot.
Simplified to run the FastAPI backend server.
For the React frontend, run: cd frontend && npm run dev
"""

import sys
import logging

from config import get_settings
from utils import setup_logging
from database import init_database, test_connection

logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI Agent Chatbot - Conversational CRUD Operations with PostgreSQL"
    )
    
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database with schema"
    )
    
    parser.add_argument(
        "--test-db",
        action="store_true",
        help="Test database connection"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Logging level. Defaults to value in .env"
    )
    
    args = parser.parse_args()
    
    try:
        # Load settings
        settings = get_settings()
        
        # Setup logging
        log_level = args.log_level or settings.log_level
        setup_logging(log_level)
        
        # Handle database initialization
        if args.init_db:
            print("\n🔧 Initializing database...")
            init_database()
            print("✅ Database initialized successfully!\n")
            return 0
        
        # Handle database test
        if args.test_db:
            print("\n🔍 Testing database connection...")
            if test_connection():
                print("✅ Database connection successful!\n")
                return 0
            else:
                print("❌ Database connection failed. Check your configuration.\n")
                return 1
        
        # Default: Run the backend server
        print("\n" + "="*60)
        print("🤖 AI Agent Chatbot - FastAPI Backend")
        print("="*60)
        print(f"\nUsing model: {settings.gemini_model}")
        print("\nStarting backend server on http://localhost:8000")
        print("\nTo use the chatbot:")
        print("  1. Backend: python main.py (this terminal)")
        print("  2. Frontend: cd frontend && npm run dev (new terminal)")
        print("  3. Open browser: http://localhost:5173")
        print("\n" + "="*60 + "\n")
        
        # Import and run backend
        from backend import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level=log_level.lower()
        )
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ Configuration error: {e}")
        print("\nPlease create a .env file based on .env.example")
        print("and configure your settings.\n")
        return 1
    
    except Exception as e:
        logger.exception("Application error")
        print(f"\n❌ An error occurred: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
