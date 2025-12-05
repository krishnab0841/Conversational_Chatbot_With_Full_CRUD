"""
Database connection and initialization module.
Handles PostgreSQL connection and database setup.
"""

import logging
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages PostgreSQL database connections."""
    
    def __init__(self):
        """Initialize database connection manager."""
        self.settings = get_settings()
        self._connection: Optional[psycopg2.extensions.connection] = None
    
    def connect(self) -> psycopg2.extensions.connection:
        """
        Establish connection to PostgreSQL database.
        
        Returns:
            psycopg2 connection object
            
        Raises:
            psycopg2.Error: If connection fails
        """
        try:
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(
                    host=self.settings.db_host,
                    port=self.settings.db_port,
                    database=self.settings.db_name,
                    user=self.settings.db_user,
                    password=self.settings.db_password,
                    cursor_factory=RealDictCursor
                )
                logger.info("Successfully connected to PostgreSQL database")
            
            return self._connection
            
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def close(self):
        """Close database connection."""
        if self._connection and not self._connection.closed:
            self._connection.close()
            logger.info("Database connection closed")
    
    def get_cursor(self):
        """
        Get a cursor for executing queries.
        
        Returns:
            psycopg2 cursor object
        """
        conn = self.connect()
        return conn.cursor()


# Global database connection instance
_db_connection: Optional[DatabaseConnection] = None


def get_db_connection() -> DatabaseConnection:
    """
    Get or create global database connection instance.
    
    Returns:
        DatabaseConnection instance
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection


def init_database():
    """
    Initialize database by creating tables from schema.
    This function reads and executes the schema.sql file.
    """
    import os
    from pathlib import Path
    
    schema_path = Path(__file__).parent / "schema.sql"
    
    if not schema_path.exists():
        logger.error(f"Schema file not found at {schema_path}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    try:
        db = get_db_connection()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        
        logger.info("Database initialized successfully")
        print("✓ Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def test_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        db = get_db_connection()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        
        logger.info("Database connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
