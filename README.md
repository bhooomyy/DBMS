# DBMS Project Documentation

## 1. Project Overview
The goal of this project is to create a lightweight, user-friendly DBMS with the following features:
- User authentication (login, signup, forgot password)
- Secure password storage using SHA-256 hashing
- User-specific folders to store databases and tables
- Support for CRUD operations on tables in .csv or other common formats
- Transaction management with concurrency control and rollback mechanisms
- Logging of all changes in .txt files
- Role-based access control (admin can grant/revoke permissions)

## 2. System Architecture
The system consists of the following components:
1. **User Authentication Module**: Handles user signup, login, and password recovery
2. **Database Storage Module**: Manages user-specific folders and table storage
3. **Table Management Module**: Implements CRUD operations on tables
4. **Transaction and Concurrency Module**: Ensures data integrity during concurrent operations
5. **Logging Module**: Tracks changes made to the database
6. **Access Control Module**: Manages user permissions

## 3. Detailed Design

### 3.1 User Authentication Module
**Features**:
- **Signup**:
  - Username (unique, primary key)
  - Password validation:
    - Minimum 8 characters
    - At least 1 capital letter
    - At least 1 special character
    - At least 1 number
  - Email (optional)
  - Passwords stored as SHA-256 hashes
- **Login**: Authenticate users using username and password
- **Forgot Password**: Allow password reset after email verification

**Implementation**:
1. Create a users table with:
   - `username` (Primary Key)
   - `password_hash` (SHA-256 hash)
   - `email` (Optional)
2. Implement password validation
3. Use SHA-256 hashing for secure password storage
4. Implement password reset mechanism

### 3.2 Database Storage Module
**Features**:
- Each user has a dedicated folder for their databases and tables
- Tables stored in .csv or other common formats

**Implementation**:
1. Create root directory (e.g., `DBMS_Root`)
2. Create user subfolders (e.g., `DBMS_Root/user1`)
3. Store all user-specific tables in their folders

### 3.3 Table Management Module
**Features**:
- CRUD operations on tables
- Support for .csv or other formats
- Additional functionalities:
  - Rename tables
  - Insert new records

**Implementation**:
1. Use pandas for .csv handling
2. Implement CRUD operation functions
3. Validate user inputs

### 3.4 Transaction and Concurrency Module
**Features**:
- Transaction support (begin, commit, rollback)
- Concurrency control using locking
- Data integrity during concurrent operations

**Implementation**:
1. Use file locks to prevent concurrent writes
2. Implement transaction logs
3. Provide rollback functionality

### 3.5 Logging Module
**Features**:
- Log all database changes
- Log format:
  - Timestamp
  - Username
  - Action (e.g., "Updated email from X to Y")
- Store logs in .txt files

**Implementation**:
1. Create logs folder in each user's directory
2. Write logs to .txt file after every operation

### 3.6 Access Control Module
**Features**:
- Admin can grant/revoke permissions
- Default: users cannot access others' databases
- Permissions include:
  - Read access
  - Write access
  - Delete access

**Implementation**:
1. Create permissions table:
   - `username`
   - `table_name`
   - `read_access` (boolean)
   - `write_access` (boolean)
   - `delete_access` (boolean)
2. Implement admin functions to update permissions

## 4. Technology Stack
- **Programming Language**: Python
- **Libraries**:
  - pandas for .csv handling
  - hashlib for SHA-256 hashing
  - os and shutil for file management
  - logging for creating logs
- **Database Storage**: File-based (.csv files)

## 5. Implementation Plan
1. **Phase 1**: User Authentication Module
2. **Phase 2**: Database Storage Module
3. **Phase 3**: Table Management Module
4. **Phase 4**: Transaction and Concurrency Module
5. **Phase 5**: Logging Module
6. **Phase 6**: Access Control Module

## 6. Testing Plan
- Unit testing for each module
- Integration testing for all modules
- Edge case testing (invalid inputs, concurrent access)

## 7. Future Enhancements
- SQL-like query support
- Indexing for faster search
- Graphical user interface (GUI)
- Additional file formats (JSON, Excel)

## 8. Conclusion
This document provides a comprehensive guide to building the DBMS. Follow the implementation plan and test thoroughly to create a robust system.
