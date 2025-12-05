"""
Input validation utilities.
"""

import re
from datetime import date, datetime
from typing import Optional, Tuple
from email_validator import validate_email as email_validate, EmailNotValidError
import phonenumbers


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validate and normalize
        email_validate(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_phone(phone: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message, formatted_phone)
    """
    try:
        # Parse phone number
        parsed = phonenumbers.parse(phone, None)
        
        # Check if valid
        if not phonenumbers.is_valid_number(parsed):
            return False, "Invalid phone number", None
        
        # Format in E164
        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        
        return True, None, formatted
        
    except phonenumbers.NumberParseException as e:
        return False, f"Invalid phone format. Use international format (e.g., +1234567890): {str(e)}", None


def validate_date(date_str: str, field_name: str = "date") -> Tuple[bool, Optional[str], Optional[date]]:
    """
    Validate and parse date string.
    Accepts formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY
    
    Args:
        date_str: Date string to validate
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (is_valid, error_message, parsed_date)
    """
    # Try different date formats
    date_formats = [
        "%Y-%m-%d",      # 2024-01-15
        "%d/%m/%Y",      # 15/01/2024
        "%m/%d/%Y",      # 01/15/2024
        "%d-%m-%Y",      # 15-01-2024
        "%m-%d-%Y",      # 01-15-2024
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str.strip(), fmt).date()
            
            # Validate date of birth constraints
            if field_name.lower() in ["date_of_birth", "dob", "birth", "birthday"]:
                if parsed_date >= date.today():
                    return False, "Date of birth must be in the past", None
                
                # Check age
                today = date.today()
                age = today.year - parsed_date.year - ((today.month, today.day) < (parsed_date.month, parsed_date.day))
                
                if age < 13:
                    return False, "You must be at least 13 years old", None
                
                if parsed_date.year < 1900:
                    return False, "Date of birth must be after 1900", None
            
            return True, None, parsed_date
            
        except ValueError:
            continue
    
    return False, f"Invalid date format. Please use YYYY-MM-DD, DD/MM/YYYY, or MM/DD/YYYY", None


def extract_field_from_message(message: str, field_name: str) -> Optional[str]:
    """
    Try to extract field value from a natural language message.
    
    Args:
        message: User message
        field_name: Field to extract
        
    Returns:
        Extracted value or None
    """
    message_lower = message.lower().strip()
    
    # Email extraction
    if field_name == "email":
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, message)
        if match:
            return match.group(0)
    
    # Phone extraction
    elif field_name == "phone_number":
        phone_pattern = r'\+?[1-9]\d{1,14}'
        match = re.search(phone_pattern, message)
        if match:
            return match.group(0)
    
    # For other fields, just return the message
    return message.strip()
