-- User Registration Database Schema
-- This schema stores user registration data with proper constraints and indexing

-- Create the database (run this separately if needed)
-- CREATE DATABASE chatbot_db;

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table to store registration data
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    CONSTRAINT check_phone_format CHECK (phone_number ~ '^\+?[1-9]\d{1,14}$'),
    CONSTRAINT check_dob_valid CHECK (date_of_birth <= CURRENT_DATE AND date_of_birth >= '1900-01-01')
);

-- Audit log table to track all operations
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    operation VARCHAR(20) NOT NULL,  -- CREATE, READ, UPDATE, DELETE
    operation_details JSONB,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT check_operation_type CHECK (operation IN ('CREATE', 'READ', 'UPDATE', 'DELETE'))
);

-- Indexes for better query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_performed_at ON audit_log(performed_at);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update updated_at on user updates
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample data for testing (optional)
-- INSERT INTO users (full_name, email, phone_number, date_of_birth, address) 
-- VALUES ('John Doe', 'john.doe@example.com', '+1234567890', '1990-01-15', '123 Main St, City, Country');
