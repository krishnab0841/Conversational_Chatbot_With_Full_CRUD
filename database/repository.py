"""
Repository pattern for database operations.
Implements all CRUD operations for users with audit logging.
"""

import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictRow

from .models import User, UserUpdate, AuditLog
from .connection import get_db_connection

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user CRUD operations with audit logging."""
    
    def __init__(self):
        """Initialize user repository."""
        self.db = get_db_connection()
    
    def _log_operation(self, operation: str, user_id: Optional[int] = None, 
                      details: Optional[Dict[str, Any]] = None):
        """
        Log operation to audit log.
        
        Args:
            operation: Type of operation (CREATE, READ, UPDATE, DELETE)
            user_id: ID of affected user
            details: Additional operation details
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT INTO audit_log (user_id, operation, operation_details)
                VALUES (%s, %s, %s)
                """,
                (user_id, operation, json.dumps(details) if details else None)
            )
            
            conn.commit()
            cursor.close()
            
        except Exception as e:
            logger.error(f"Failed to log operation: {e}")
    
    def create(self, user: User) -> User:
        """
        Create a new user registration.
        
        Args:
            user: User object with registration data
            
        Returns:
            Created user with ID
            
        Raises:
            ValueError: If email already exists
            psycopg2.Error: If database operation fails
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT INTO users (full_name, email, phone_number, date_of_birth, address)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, full_name, email, phone_number, date_of_birth, address, 
                          created_at, updated_at
                """,
                (user.full_name, user.email, user.phone_number, 
                 user.date_of_birth, user.address)
            )
            
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            
            created_user = User(**dict(result))
            
            # Log operation
            self._log_operation("CREATE", created_user.id, {"email": user.email})
            
            logger.info(f"Created user with ID: {created_user.id}")
            return created_user
            
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise ValueError(f"Email {user.email} is already registered")
            raise
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to create user: {e}")
            raise
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT id, full_name, email, phone_number, date_of_birth, address,
                       created_at, updated_at
                FROM users
                WHERE email = %s
                """,
                (email,)
            )
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                user = User(**dict(result))
                self._log_operation("READ", user.id, {"email": email})
                return user
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve user by email: {e}")
            raise
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT id, full_name, email, phone_number, date_of_birth, address,
                       created_at, updated_at
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                user = User(**dict(result))
                self._log_operation("READ", user.id)
                return user
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve user by ID: {e}")
            raise
    
    def update(self, email: str, updates: UserUpdate) -> Optional[User]:
        """
        Update user information.
        
        Args:
            email: Email of user to update
            updates: UserUpdate object with fields to update
            
        Returns:
            Updated user object if found, None otherwise
        """
        try:
            # Build dynamic update query
            update_fields = []
            values = []
            
            for field, value in updates.model_dump(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            if not update_fields:
                logger.warning("No fields to update")
                return self.get_by_email(email)
            
            # Add email to values for WHERE clause
            values.append(email)
            
            conn = self.db.connect()
            cursor = conn.cursor()
            
            query = f"""
                UPDATE users
                SET {', '.join(update_fields)}
                WHERE email = %s
                RETURNING id, full_name, email, phone_number, date_of_birth, address,
                          created_at, updated_at
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            
            if result:
                updated_user = User(**dict(result))
                self._log_operation("UPDATE", updated_user.id, 
                                  {"updated_fields": list(updates.model_dump(exclude_unset=True).keys())})
                logger.info(f"Updated user ID: {updated_user.id}")
                return updated_user
            
            return None
            
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise ValueError(f"Email {updates.email} is already registered")
            raise
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update user: {e}")
            raise
    
    def delete(self, email: str) -> bool:
        """
        Delete user registration.
        
        Args:
            email: Email of user to delete
            
        Returns:
            True if deleted, False if user not found
        """
        try:
            # Get user first for audit log
            user = self.get_by_email(email)
            if not user:
                return False
            
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM users WHERE email = %s",
                (email,)
            )
            
            deleted = cursor.rowcount > 0
            conn.commit()
            cursor.close()
            
            if deleted:
                self._log_operation("DELETE", user.id, {"email": email})
                logger.info(f"Deleted user with email: {email}")
            
            return deleted
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to delete user: {e}")
            raise
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """
        List all users with pagination.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List of User objects
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT id, full_name, email, phone_number, date_of_birth, address,
                       created_at, updated_at
                FROM users
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            
            results = cursor.fetchall()
            cursor.close()
            
            return [User(**dict(row)) for row in results]
            
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            raise
