# Secure Task Manager 

A secure Django-based task management application developed for the **Security of Web Applications** course.  
This project demonstrates practical implementations of authentication, authorization, input validation, audit logging, and common web security best practices.

---

## Project Overview

The goal of this project is to build a **simple but security-focused web application** that satisfies core web application security requirements.

The application allows users to manage personal tasks while strictly enforcing access control and user data isolation.

---

## 1. Authentication (Registration & Login)

### Registration

- Users can register with a username and password
- Passwords are **never stored in plaintext**
- Django’s built-in password hashing (**PBKDF2**) is used automatically
- Invalid inputs trigger validation errors (e.g. weak passwords, mismatched confirmation)

**Enforced by:**
- `RegisterForm` (Django `UserCreationForm`)
- `AUTH_PASSWORD_VALIDATORS` in `settings.py`

---

### Login

- Users can log in with valid credentials
- Failed login attempts do not leak sensitive information
- Authentication state is maintained using a **secure session cookie**

**Security features:**
- Failed login attempts are logged
- Session cookies are `HttpOnly` and `SameSite`

---

## 2. Authorization & Access Control

### Protected Routes

- Access without login is denied
- Only authenticated users can access task-related endpoints

**Enforced by:**
- `@login_required` decorator in Django views

---

### Role-Based Access

- Regular users **cannot access** the Django admin panel
- Only superusers see the **Admin Panel** button in the UI

---

### User Data Isolation (CRITICAL)

- User A can create tasks
- User B **cannot**:
  - View User A’s tasks
  - Modify User A’s tasks
  - Delete User A’s tasks

**Enforced by:**
- Query filtering:
  ```python
  Task.objects.filter(owner=request.user)
