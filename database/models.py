"""
Data models for the chatbot application.
Defines User and AuditLog models with validation.
"""

from datetime import date, datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator
import phonenumbers


class User(BaseModel):
    """User registration data model."""
    
    id: Optional[int] = None
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address")
    phone_number: str = Field(..., description="Phone number in international format")
    date_of_birth: date = Field(..., description="Date of birth")
    address: str = Field(..., min_length=5, description="Full address")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Validate phone number format using phonenumbers library."""
        try:
            # Parse phone number
            parsed = phonenumbers.parse(v, None)
            
            # Check if valid
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            
            # Return in E164 format
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
        except phonenumbers.NumberParseException:
            raise ValueError(f"Invalid phone number format: {v}. Please use international format (e.g., +1234567890)")
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        """Validate that date of birth is in the past and person is at least 13 years old."""
        if v >= date.today():
            raise ValueError("Date of birth must be in the past")
        
        # Calculate age
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        
        if v.year < 1900:
            raise ValueError("Date of birth must be after 1900")
        
        return v
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone_number": "+1234567890",
                "date_of_birth": "1990-01-15",
                "address": "123 Main St, New York, NY 10001, USA"
            }
        }


class UserUpdate(BaseModel):
    """Model for updating user data - all fields optional."""
    
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = Field(None, min_length=5)
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format if provided."""
        if v is None:
            return v
        
        try:
            parsed = phonenumbers.parse(v, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError(f"Invalid phone number format: {v}")
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: Optional[date]) -> Optional[date]:
        """Validate date of birth if provided."""
        if v is None:
            return v
        
        if v >= date.today():
            raise ValueError("Date of birth must be in the past")
        
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        
        if v.year < 1900:
            raise ValueError("Date of birth must be after 1900")
        
        return v


class AuditLog(BaseModel):
    """Audit log entry model."""
    
    id: Optional[int] = None
    user_id: Optional[int] = None
    operation: str = Field(..., pattern="^(CREATE|READ|UPDATE|DELETE)$")
    operation_details: Optional[Dict[str, Any]] = None
    performed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
